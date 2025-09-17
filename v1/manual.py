from ipa_converter import convert_table_to_ipa, convert_code_to_ipa, convert_table_from_ipa
from table_reader import read_vocab, write_vocab
from sound_change import read_sound_change
from vocab import Vocab

# coni = input("input converter file name> ")
# inp = input("input data file name> ")
# cod = input("input code file name> ")
# outp = input("input output file name> ")
# cono = input("input converter output file name> ")
def get(a, b):
    return input(a + " from " + b + " > ")
def lit(_,b):
    return b
def run(coni, inp, cod, outp, cono):
    conv = open(coni, "r").read()
    data = convert_table_to_ipa(open(inp, "r").read(), conv)
    vocab: Vocab = read_vocab(data)
    code = convert_code_to_ipa(open(cod, "r").read(), conv)
    sound_change = read_sound_change(code)

    for lineix in range(len(sound_change[0])):
        c = sound_change[1][lineix]
        if sound_change[2][lineix]:
            delete = sound_change[1][lineix]
            if delete is not None:
                vocab.rem_grammar(delete[0])
        elif c is None:
            vocab.modify(sound_change[0][lineix])
        elif sound_change[3][lineix]:
            (new, old) = c
            vocab.add_grammar(sound_change[0][lineix], lit, new, old)
        else:
            (new, old) = c
            vocab.add_grammar(sound_change[0][lineix], get, new, old)

    (out, conv_out) = convert_table_from_ipa(write_vocab(vocab), conv)
    open(outp, "w").write(out)
    open(cono, "w").write(conv_out)