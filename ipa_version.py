from table_reader import read_vocab, write_vocab
from vocab import Vocab
from typing import Callable
from sound_change import read_sound_change

def run_ipa():
    filename = input("input data file name> ")
    data = open(filename, "r").read()
    vocab: Vocab = read_vocab(data)

    filename = input("input code file name> ")
    code = open(filename, "r").read()
    sound_change = read_sound_change(code)

    filename = input("input output file name> ")

    for lineix in range(len(sound_change[0])):
        c = sound_change[1][lineix]
        if c is None:
            vocab.modify(sound_change[0][lineix])
        else:
            (new, old) = c
            vocab.add_grammar(sound_change[0][lineix], new, old)

    open(filename, "w").write(write_vocab(vocab))

