from typing import Any, Callable
from phoneme import phoneme, phoneme_mod

class renderer:
    def __init__(self, data: dict[phoneme, str], source: Callable[[phoneme], str]) -> None:
        self.source = source
        self.data = data
        self.cache = []
    def __call__(self, *args: phoneme) -> str:
        return "".join([self.data[arg] if arg in self.data else (self.data.update({arg: self.source(arg)}) or self.cache.append(arg) or self.data[arg]) for arg in args])
    def reset_cache(self):
        self.cache = []
    def clean_data(self):
        self.data = dict([(a, self.data[a]) for a in self.data if a in self.cache])
    def reverse(self):
        d = {}
        for a in self.data:
            d[self.data[a]] = a
        return d
    def split(self, s: str):
        out: list[phoneme] = []
        while s != "":
            possibilities = []
            for beginning in [s[:a] for a in range(1,len(s))]:
                if beginning in self.data:
                    possibilities.append(len(beginning))
            length = max(possibilities)
            out.append(self.reverse()[s[:length]])
            s = s[length:]
        return out
class mod_renderer:
    def __init__(self, data: Callable[[str], phoneme_mod], validator: Callable[[str], bool]) -> None:
        self.data = data
        self.validator = validator
    def split(self, s: str):
        out: list[phoneme_mod] = []
        while s != "":
            possibilities = []
            for beginning in [s[:a] for a in range(1,len(s))]:
                if self.validator(beginning):
                    possibilities.append(len(beginning))
            length = max(possibilities)
            out.append(self.data(s[:length]))
            s = s[length:]
        return out
    