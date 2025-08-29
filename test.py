from sound_change import *
from ipa import *
from vocab import *

vocab = Vocab([["x", "y"], ["---", "---"],["a", "b"], ["c", "d"]])
sound_change = read_sound_change("""
```
GRM
z : k \\  _ # ; x
```
"""
)
for lineix in range(len(sound_change[0])):
    c = sound_change[1][lineix]
    if c is None:
        vocab.modify(sound_change[0][lineix])
    else:
        (new, old) = c
        vocab.add_grammar(sound_change[0][lineix], new, old)

print(vocab.to_list())