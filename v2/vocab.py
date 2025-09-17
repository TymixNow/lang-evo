from phoneme import phoneme
from phoneme_renderer import renderer
from typing import Callable
class Vocab:
    def __init__(self, table: list[list[tuple[str, list[phoneme]]]], headers: list[str]) -> None:
        self.data = table
        self.headers = headers
        self.selection: list[int] = []
    def select(self, header_predicate: Callable[[str], bool]) -> None:
        self.selection = [i for i in range(len(self.headers)) if header_predicate(self.headers[i])]
        return
    def get_selection(self):
        return [[line[i] for i in range(len(line)) if i in self.selection] for line in self.data]
    def get_selected_headers(self):
        return [self.headers[i] for i in range(len(self.headers)) if i in self.selection]
    def set_in_selection(self, x: int, y: int, value: tuple[str, list[phoneme]]):
        self.data[x][self.selection[y]] = value
    def __contains__(self, obj: str):
        return obj in [a[0] for b in self.get_selection() for a in b]
    def modify_values(self, mod: Callable[[list[phoneme]], list[phoneme]]):
        for x in range(len(self.get_selection())):
            line = self.get_selection()[x]
            for y in range(len(line)):
                cell = line[y]
                self.set_in_selection(x,y,(cell[0],mod(cell[1])))
    def modify_keys(self, mod: Callable[[str], str]):
        for x in range(len(self.get_selection())):
            line = self.get_selection()[x]
            for y in range(len(line)):
                cell = line[y]
                self.set_in_selection(x,y,(mod(cell[0]),cell[1]))
    def copy_columns(self):
        width = len(self.headers)
        delta = len(self.selection)
        self.headers += self.get_selected_headers()
        for x in range(len(self.data)):
            self.data[x] += self.get_selection()[x]
        self.selection = list(range(width, width + delta))
    def rename_columns(self, mod: Callable[[str], str]):
        for a in self.selection: self.headers[a] = mod(self.headers[a])
    def delete_columns(self):
        copy = self
        copy.headers = [copy.headers[i] for i in range(len(copy.headers)) if i not in copy.selection]
        copy.data = [[line[i] for i in range(len(line)) if i not in copy.selection] for line in copy.data]
        self = copy
    


        
