from table_reader import read_vocab, write_vocab
from ipa import split_ipa
from vocab import Vocab

def convert_to_ipa(inp: str, conv: str) -> str:
    vocab = read_vocab(conv)
    for char in [a[0] for a in vocab]:
        inp = inp.replace(char, "".join([str(a) for a in vocab[char]]))
    return inp

def convert_from_ipa(inp: str, conv: str, conv_pipe: str) -> tuple[str, str]:
    vocab = dict(zip([a[0] for a in dict(read_vocab(conv)).values()], dict(read_vocab(conv)).keys()))
    vocab_pipe = dict(zip([a[0] for a in dict(read_vocab(conv_pipe)).values()], dict(read_vocab(conv_pipe)).keys()))
    out = ""
    for char in split_ipa(inp):
        if char not in vocab.keys() and char not in vocab_pipe.keys():
            vocab_pipe[char] = input("transcription for \"" + str(char) + "\" > ")
        elif char in vocab.keys():
            vocab_pipe[char] = vocab[char]
        out += vocab_pipe[char]
    new = write_vocab(Vocab([["     ", "     "],[" --- ", " --- "]] + [list(x) for x in zip(vocab_pipe.values(), [str(key) for key in vocab_pipe.keys()])]))
    return (out, new)

def convert_table_to_ipa(table: str, conv: str) -> str:
    lines: list[str] = table.split("\n")
    while lines[0].strip() == "": lines = lines[1:]
    while lines[-1].strip() == "": lines = lines[:-1]
    prefix = lines[1].split("|")[0]
    suffix = lines[1].split("|")[-1]
    prefix = prefix + "|" if prefix.strip() == "" else ""
    suffix = suffix + "|" if suffix.strip() == "" else ""
    cells: list[list[str]] = [[cell.strip() for cell in line.removeprefix(prefix).removesuffix(suffix).split("|")] for line in lines]
    cells_p = [[(key, convert_to_ipa(val, conv)) for (key, val) in zip(line[0::2], line[1::2])] for line in cells]
    cells = [[a for b in line for a in b] for line in cells_p]
    widths = [0 for _ in cells[0]]
    for row in cells:
        for col in range(len(row)):
            widths[col] = max([widths[col], len(row[col])])
    for row in range(len(cells)):
        for col in range(len(cells[0])):
            if len(cells[row]) > col:
                cells[row][col] = " " + cells[row][col] + ((widths[col] - len(cells[row][col]) + 1) * " ")
            else:
                cells[row].append(" "*(widths[col]+2))
    lines = ["|" + "|".join(line) + "|" for line in cells]
    return "\n".join(lines)

def convert_table_from_ipa(table: str, conv: str) -> tuple[str,str]:
    lines: list[str] = table.split("\n")
    while lines[0].strip() == "": lines = lines[1:]
    while lines[-1].strip() == "": lines = lines[:-1]
    prefix = lines[1].split("|")[0]
    suffix = lines[1].split("|")[-1]
    prefix = prefix + "|" if prefix.strip() == "" else ""
    suffix = suffix + "|" if suffix.strip() == "" else ""
    cells: list[list[str]] = [[cell.strip() for cell in line.removeprefix(prefix).removesuffix(suffix).split("|")] for line in lines]
    cells = [cells[0]] + cells[2:]
    cells_p = []
    conv_out = "|     |     |\n| --- | --- |"
    for line in cells:
        cells_p_line = []
        for (key, val) in zip(line[0::2], line[1::2]):
            (out, conv_out) = convert_from_ipa(val, conv,  conv_out)
            cells_p_line.append((key, out))
        cells_p.append(cells_p_line)
    cells = [[a for b in line for a in b] for line in cells_p]
    widths = [0 for _ in cells[0]]
    for row in cells:
        for col in range(len(row)):
            widths[col] = max([widths[col], len(row[col])])
    for row in range(len(cells)):
        for col in range(len(cells[0])):
            if len(cells[row]) > col:
                cells[row][col] = " " + cells[row][col] + ((widths[col] - len(cells[row][col]) + 1) * " ")
            else:
                cells[row].append(" "*(widths[col]+2))
    line1 = "".join(["|" + ((widths[col] +2) * "-") for col in range(len(widths))]) + "|"
    lines = ["|" + "|".join(line) + "|" for line in cells]
    return "\n".join([lines[0]] + [line1] + lines[1:]), conv_out

def convert_code_to_ipa(inp: str, conv: str):
    out: list[str] = []
    for line in inp.split("\n"): 
        pre = ""
        post = ""
        mid = line
        if ":" in line:
            pre = mid.split(":",1)[0] + ":"
            mid = mid.split(":",1)[1]
        if ";" in line:
            post = ";" + mid.split(";",1)[1]
            mid = mid.split(";",1)[0]
        out.append(pre + convert_to_ipa(mid,conv) + post)
    return "\n".join(out)