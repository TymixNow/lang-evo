from ipa import *
from typing import Callable
class Vocab:
    def __init__(self, double_table: list[list[str]] = []) -> None:
        self.data: list[list[tuple[str,list[phoneme]]]] = [[(a, split_ipa(b)) if a!="" and b!="" else ("", []) for (a,b) in zip(line[0::2], line[1::2])] for line in double_table[2:]]
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
        body = [[s for pair in line for s in (pair[0], "".join([render(ph) for ph in pair[1]]))] for line in self.data]
        return [[s for pair in self.headers for s in pair]] + body