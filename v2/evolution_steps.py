from typing import Callable, Optional
from phoneme import phoneme, phoneme_kind, phoneme_mod

def match_ph(matcher: list[phoneme_kind], matchee: list[phoneme], begin: bool, end: bool):
    starts: set[int] = set()
    for start in range(len(matchee) - len(matcher) + 1):
        possible = True
        for index in range(len(matcher)):
            possible = (matchee[start + index] in matcher[index])
            if not possible: break
        if possible:
            starts.add(start)
    if begin: starts = set([0]) & starts
    if end: starts = set([len(matchee) - len(matcher)]) & starts
    return starts

def evolve(pre: list[phoneme_kind], mid: list[phoneme_kind], post: list[phoneme_kind], repl: list[Optional[phoneme_mod]], begin: bool, end: bool):
    matcher = pre + mid + post
    offset = len(pre)
    def mod(word: list[phoneme]) -> list[phoneme]:
        starts: set[int] = match_ph(matcher, word, begin, end)
        temp: list[phoneme | None] = [a for a in word]
        for start in starts:
            for index in range(len(repl)):
                char = repl[index]
                a = temp[start + index + offset]
                if char is None or a is None:
                    temp[start + index + offset] = None
                else:
                    temp[start + index + offset] = char(a)
        out: list[phoneme] = []
        for ph in temp:
            if ph is not None: out.append(ph)
        return out
    return mod

def metathesise(pre: list[phoneme_kind], first: list[phoneme_kind], second: list[phoneme_kind], post: list[phoneme_kind], begin: bool, end: bool):
    matcher = pre + first + second + post
    offset = len(pre)
    def mod(word: list[phoneme]) -> list[phoneme]:
        starts: set[int] = match_ph(matcher, word, begin, end)
        out: list[phoneme] = [a for a in word]
        for start in [a + offset for a in starts]:
            inside = word[start:start + len(first + second)]
            inside = inside[len(first):] + inside[:len(first)]
            out = out[:start] + inside + out[(start + len(first + second)):]
        return out
    return mod

def epenthesise(pre: list[phoneme_kind], insert: list[phoneme], post: list[phoneme_kind], begin: bool, end: bool):
    matcher = pre + post
    offset = len(pre)
    def mod(word: list[phoneme]) -> list[phoneme]:
        if word != []:
            starts: set[int] = match_ph(matcher, word, begin, end)
            out: list[phoneme] = [a for a in word]
            for start in [a + offset for a in starts]:
                out = out[:start] + insert + out[start:]
            return out
        else:
            return []
    return mod
