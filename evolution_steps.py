from typing import Optional
from ipa import phoneme, phoneme_group, phoneme_mod, contained

def match_ph(matcher: list[phoneme_group], matchee: list[phoneme], begin: bool, end: bool):
    starts: set[int] = set()
    for start in range(len(matchee) - len(matcher) + 1):
        possible = True
        for index in range(len(matcher)):
            possible = contained(matchee[start + index], matcher[index])
            if not possible: break
        if possible:
            starts.add(start)
    if begin: starts = set([0]) & starts
    if end: starts = set([len(matchee) - len(matcher)]) & starts
    return starts

def evolve_leq(pre: list[phoneme_group], mid: list[phoneme_group], post: list[phoneme_group], repl: list[Optional[phoneme_mod]], begin: bool, end: bool):
    matcher = pre + mid + post
    offset = len(pre)
    def mod(word: list[phoneme]) -> list[phoneme]:
        starts: set[int] = match_ph(matcher, word, begin, end)
        temp: list[phoneme | None] = [a for a in word]
        for start in starts:
            for index in range(len(repl)):
                char = matcher[index]
                a = temp[start + index + offset]
                if char is None or a is None:
                    temp[start + index + offset] = None
                else:
                    temp[start + index + offset] = a.apply(repl[index])
        out: list[phoneme] = []
        for ph in temp:
            if ph is not None: out.append(ph)
        return out
    return mod

def metathesise(pre: list[phoneme_group], first: list[phoneme_group], second: list[phoneme_group], post: list[phoneme_group], begin: bool, end: bool):
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

def epenthesise(pre: list[phoneme_group], insert: list[phoneme], post: list[phoneme_group], begin: bool, end: bool):
    matcher = pre + post
    offset = len(pre)
    def mod(word: list[phoneme]) -> list[phoneme]:
        starts: set[int] = match_ph(matcher, word, begin, end)
        out: list[phoneme] = [a for a in word]
        for start in [a + offset for a in starts]:
            out = out[:start] + insert + out[start:]
        return out
    return mod
