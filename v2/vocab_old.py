from phoneme import phoneme
from phoneme_renderer import renderer
from typing import Callable
class Vocab:
    def __init__(self, rend: renderer,  double_table: list[list[str]] = []) -> None:
        self.rend: renderer = rend
        self.data: list[list[tuple[str,list[phoneme]]]] = [[(a, self.rend.split(b)) if a!="" and b!="" else ("", []) for (a,b) in zip(line[0::2], line[1::2])] for line in double_table[2:]]
        self.headers: list[tuple[str,str]] = [(a,b) for (a,b) in zip(double_table[0][0::2], double_table[0][1::2])]
    def to_list_flat(self):
        l: list[tuple[str, list[phoneme]]] = []
        for x in [a for b in self.data for a in b]: 
            if x not in l: l.append(x)
        return l
    def __iter__(self):
        yield from self.to_list_flat()
    def __getitem__(self, word):
        return dict(self.to_list_flat())[word]
    def __setitem__(self, word, value):
        for (j,i) in [(j,i) for j in range(len(self.data)) for i in range(len(self.data[j])) if self.data[j][i][0] == word]: self.data[j][i] = (self.data[j][i][0], value) 
    def modify(self, mod: Callable):
        for word in self:
            self[word[0]] = mod(word[1])
    def add_grammar(self, mod: Callable, get: Callable, new_header: str, old_headers: list[str] | None = None):
        if old_headers is None: old_headers = [a[0] for a in self.headers]
        old_header_ixs = [[b[0] for b in self.headers].index(a) for a in old_headers]
        new_headers = [(new_header,"") for a in old_headers]
        self.headers.extend(new_headers)
        for j in range(len(self.data)):
            line = self.data[j]
            add = []
            for ix in range(len(old_header_ixs)):
                i = old_header_ixs[ix]
                cell = line[i]
                if cell[0] != "":
                    inp = get(new_headers[ix][0], cell[0])
                    if inp != "":
                        add.append((inp,mod(cell[1])))
                    else:
                        add.append(("", []))
                else:
                    add.append(("", []))
            self.data[j].extend(add)
    def rem_grammar(self, header: str):
        rems = [i for i in range(len(self.headers)) if self.headers[i][0].strip() == header.strip()]
        if rems == []: print(rems)
        rem_index = [i for i in range(len(self.headers)) if self.headers[i][0].strip() == header.strip()][0]
        self.headers = self.headers[:rem_index] + self.headers[rem_index + 1:]
        self.data = [line[:rem_index] + line[rem_index + 1:] for line in self.data]
    def to_list(self) -> list[list[str]]:
        body = [[s for pair in line for s in (pair[0], "".join([self.rend(ph) for ph in pair[1]]))] for line in self.data]
        return [[s for pair in self.headers for s in pair]] + body
    @classmethod
    def read(cls, table: str, rend: renderer):
        lines: list[str] = table.split("\n")
        while lines[0].strip() == "": lines = lines[1:]
        while lines[-1].strip() == "": lines = lines[:-1]
        prefix = lines[1].split("|")[0]
        suffix = lines[1].split("|")[-1]
        prefix = prefix + "|" if prefix.strip() == "" else ""
        suffix = suffix + "|" if suffix.strip() == "" else ""
        cells: list[list[str]] = [[cell.strip() for cell in line.removeprefix(prefix).removesuffix(suffix).split("|")] for line in lines]
        return Vocab(rend, cells)
    def write(self) -> str:
        cells = self.to_list()
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