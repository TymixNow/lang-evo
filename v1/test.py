from sound_change import *
from ipa import *
from vocab import *

vocab = Vocab([["x", "y"], ["---", "---"],["a", "b"], ["c", "dʕ"]])
sound_change = read_sound_change(
"""
```
EVO
d > d̪ \\ _ʕh ;
bdd̪ɡ > vzxhʕ \\ _ʕh ;
```
"""
)

def get(a, b):
    return input(a + " from " + b + " > ")
def lit(_,b):
    return b
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
    print([[str(b) for b in a[1]] for a in vocab])

print(vocab.to_list())