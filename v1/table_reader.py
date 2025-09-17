from vocab import Vocab
def read_vocab(table: str) -> Vocab:
    lines: list[str] = table.split("\n")
    while lines[0].strip() == "": lines = lines[1:]
    while lines[-1].strip() == "": lines = lines[:-1]
    prefix = lines[1].split("|")[0]
    suffix = lines[1].split("|")[-1]
    prefix = prefix + "|" if prefix.strip() == "" else ""
    suffix = suffix + "|" if suffix.strip() == "" else ""
    cells: list[list[str]] = [[cell.strip() for cell in line.removeprefix(prefix).removesuffix(suffix).split("|")] for line in lines]
    return Vocab(cells)
    
def write_vocab(vocab: Vocab) -> str:
    cells = vocab.to_list()
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
    return "\n".join([lines[0]] + [line1] + lines[1:])