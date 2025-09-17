import types
from functools import reduce
"""
syll cons appx son
voice spr_glot con_glot
cont nas strid lat del_rel
"""
#0100_0_10_0000_00_0100_100_10000
"""
labial round
coronal ant dist
dorsal high low back tense
radical atr rtr
"""

class phoneme:
    renderer = {}
    def __init__(self,x: int,y: int) -> None:
        x = x & 0x1FFF
        y = y & 0xFFF
        self.data = y | (x << 12)
    def __and__(self,other):
        new = self.data & other.data
        x = (new >> 12) & 0x1FFF
        y = new & 0xFFF
        return phoneme(x,y)
    def __or__(self,other):
        new = self.data | other.data
        x = (new >> 12) & 0x1FFF
        y = new & 0xFFF
        return phoneme(x,y)
    def __xor__(self,other):
        new = self.data ^ other.data
        x = (new >> 12) & 0x1FFF
        y = new & 0xFFF
        return phoneme(x,y)
    def __invert__(self):
        new = 0x1FFFFFF ^ self.data
        x = (new >> 12) & 0x1FFF
        y = new & 0xFFF
        return phoneme(x,y)
    def apply(self, mod):
        return (self & mod[1]) | mod[0]
    def __str__(self):
        setrenederer()
        print("{0:25b}".format(self.data).replace(" ", "0"))
        return dict(zip(phoneme.renderer.values(), phoneme.renderer.keys()))[self]
    def __eq__(self, value: object) -> bool:
        match value:
            case phoneme():
                return self.data == value.data
            case int():
                return False
                #return self.data == value
            case _:
                return False
    def __hash__(self) -> int:
        return hash(self.data)
    def __getitem__(self, index: str | int):
        l_s = "labial coronal dorsal radical round ant dist high low back tense atr rtr syll cons appx son voice spr_glot con_glot cont nas strid lat del_rel"
        l = [str(x) for x in list(reversed(l_s.split()))]
        i = 0
        match index:
            case int():
                i = index
            case str():
                i = l.index(index)
            case _:
                raise TypeError(index)
        return 1 & self.data >> i == 1
    def __setitem__(self, index, value):
        l_s = "labial coronal dorsal radical round ant dist high low back tense atr rtr syll cons appx son voice spr_glot con_glot cont nas strid lat del_rel"
        l = [str(x) for x in list(reversed(l_s.split()))]
        i = 0
        match index:
            case int():
                i = index
            case str():
                i = l.index(index)
            case _:
                raise TypeError(index)
        self.data = (int(value) << i | self.data) & (~ int(not value) << i)
phoneme_mod = tuple[phoneme,phoneme]
phoneme_group = phoneme_mod
class IPA:
    plosive     = 0b0100_000_00000
    implosive   = 0b0100_001_00000
    ejective    = 0b1100_001_00000
    nasal       = 0b0101_000_11000
    trill       = 0b0101_000_10000
    tap         = 0b0101_000_00000
    fricative   = 0b0100_000_10000
    strident    = 0b0100_000_10100
    affricate   = 0b0100_000_10001
    lateral     =          0b00010
    approximant = 0b0111_000_10000
    click       = 0b1101_001_00000

    syllabic    = 0b1000_000_00000
    voiced      =      0b100_00000
    aspirated   =      0b010_00000
    nasalised   =          0b01000


    bilabial       = 0b1000_0_00_0000_00
    labiodental    = 0b1100_0_00_0000_00
    dental         = 0b0100_0_11_0000_00
    alveolar       = 0b0100_0_10_0000_00 #strident for sibilant
    postalveolar   = 0b0100_0_01_0000_00
    retroflex      = 0b0100_0_00_0000_00
    alveolopalatal = 0b0110_0_10_1000_00
    palatal        = 0b0010_0_00_1000_00
    labiovelar     = 0b1010_0_00_0100_00
    velar          = 0b0010_0_00_0100_00
    uvular         = 0b0010_0_00_0110_00
    pharyngeal     = 0b0001_0_00_0000_01
    epiglottal     = 0b0001_0_00_0000_00
    glottal        = 0b0000_0_00_0000_00

    labialized     = 0b1000_1_00_0000_00


    vowel_manner = 0b1001_100_10000
    vow_breathy  = 0b1001_110_10000
    vow_creaky   = 0b1001_101_10000

    vow_high       = 0b0010_0_00_1000_00
    vow_mid        = 0b0010_0_00_0000_00
    vow_low        = 0b0010_0_00_0100_00
    vow_back       = 0b0010_0_00_0010_00
    vow_rounded    = 0b1010_1_00_0000_00


    ipa_consonants: dict[str,phoneme] = {
        "\u0070": phoneme(bilabial,plosive),
        "\u0062": phoneme(bilabial,voiced | plosive),
        "\u0070\u032a": phoneme(labiodental,plosive),
        "\u0062\u032a": phoneme(labiodental,voiced | plosive),
        "\u0074\u032a": phoneme(dental,plosive),
        "\u0064\u032a": phoneme(dental,voiced | plosive),
        "\u0074": phoneme(alveolar,plosive),
        "\u0064": phoneme(alveolar,voiced | plosive),
        "\u0288": phoneme(retroflex,plosive),
        "\u0256": phoneme(retroflex,voiced | plosive),
        "\u0236": phoneme(alveolopalatal,plosive),
        "\u0221": phoneme(alveolopalatal,voiced | plosive),
        "\u0063": phoneme(palatal,plosive),
        "\u025f": phoneme(palatal,voiced | plosive),
        "\u006b\u0361\u0070": phoneme(labiovelar,plosive),
        "\u0261\u0361\u0062": phoneme(labiovelar,voiced | plosive),
        "\u006b": phoneme(velar,plosive),
        "\u0261": phoneme(velar,voiced | plosive),
        "\u0071": phoneme(uvular,plosive),
        "\u0262": phoneme(uvular,voiced | plosive),
        "\u02a1": phoneme(epiglottal,plosive),
        "\u0294": phoneme(glottal,plosive),

        "\u0253\u0325": phoneme(bilabial,implosive),
        "\u0253": phoneme(bilabial,voiced | implosive),
        "\u0257\u032a": phoneme(dental,voiced | implosive),
        "\u0257": phoneme(alveolar,voiced | implosive),
        "\u1d91": phoneme(retroflex,voiced | implosive),
        "\u0284": phoneme(palatal,voiced | implosive),
        "\u0260": phoneme(velar,voiced | implosive),
        "\u029b": phoneme(uvular,voiced | implosive),

        "\u0070\u02bc": phoneme(bilabial,ejective),
        "\u0074\u032a\u02bc": phoneme(dental,ejective),
        "\u0074\u02bc": phoneme(alveolar,ejective),
        "\u0288\u02bc": phoneme(retroflex,ejective),
        "\u0063\u02bc": phoneme(palatal,ejective),
        "\u006b\u02bc": phoneme(velar,ejective),
        "\u0071\u02bc": phoneme(uvular,ejective),

        "\u006d\u0325": phoneme(bilabial,nasal),
        "\u006d": phoneme(bilabial,voiced | nasal),
        "\u0271\u0325": phoneme(labiodental,nasal),
        "\u0271": phoneme(labiodental,voiced | nasal),
        "\u006e\u032a\u030a": phoneme(dental,nasal),
        "\u006e\u032a": phoneme(dental,voiced | nasal),
        "\u006e\u0325": phoneme(alveolar,nasal),
        "\u006e": phoneme(alveolar,voiced | nasal),
        "\u0273\u030a": phoneme(retroflex,nasal),
        "\u0273": phoneme(retroflex,voiced | nasal),
        "\u0235": phoneme(alveolopalatal,voiced | nasal),
        "\u0272": phoneme(palatal,voiced | nasal),
        "\u014b\u0361\u006d": phoneme(labiovelar,voiced | nasal),
        "\u014b": phoneme(velar,voiced | nasal),
        "\u0274": phoneme(uvular,voiced | nasal),

        "\u0299": phoneme(bilabial,voiced | trill),
        "\u0072\u0325": phoneme(alveolar,trill),
        "\u0072": phoneme(alveolar,voiced | trill),
        "\u0280": phoneme(uvular,voiced | trill),

        "\u2c71\u031f": phoneme(bilabial,voiced | tap),
        "\u2c71": phoneme(labiodental,voiced | tap),
        "\u027e": phoneme(alveolar,tap),
        "\u027d": phoneme(alveolar,voiced | tap),

        "\u027a": phoneme(alveolar, lateral | tap),
        "\U0001df08": phoneme(retroflex, lateral | tap),

        "\u0278": phoneme(bilabial,fricative),
        "\u03b2": phoneme(bilabial,voiced | fricative),
        "\u0066": phoneme(labiodental,strident | fricative),
        "\u0076": phoneme(labiodental,strident | voiced | fricative),
        "\u03b8": phoneme(dental,fricative),
        "\u00f0": phoneme(dental,voiced | fricative),
        "\u0073": phoneme(alveolar,strident | fricative),
        "\u007a": phoneme(alveolar,strident | voiced | fricative),
        "\u0283": phoneme(postalveolar,strident | fricative),
        "\u0292": phoneme(postalveolar,strident | voiced | fricative),
        "\u0282": phoneme(retroflex,strident | fricative),
        "\u0290": phoneme(retroflex,strident | voiced | fricative),
        "\u0255": phoneme(alveolopalatal,strident | fricative),
        "\u0291": phoneme(alveolopalatal,strident | voiced | fricative),
        "\u00e7": phoneme(palatal,fricative),
        "\u029d": phoneme(palatal,voiced | fricative),
        "\u0078": phoneme(velar,fricative),
        "\u0263": phoneme(velar,voiced | fricative),
        "\u03c7": phoneme(uvular,strident | fricative),
        "\u0281": phoneme(uvular,strident | voiced | fricative),
        "\u0127": phoneme(pharyngeal,fricative),
        "\u0295": phoneme(pharyngeal,voiced | fricative),
        "\u029c": phoneme(epiglottal,fricative),
        "\u02a2": phoneme(epiglottal,voiced | fricative),
        "\u0068": phoneme(glottal,fricative),
        "\u0266": phoneme(glottal,voiced | fricative),

        "\u026c": phoneme(alveolar, lateral | fricative),
        "\u026e": phoneme(alveolar, lateral | voiced | fricative),
        "\ua78e": phoneme(retroflex, lateral | fricative),

        "\u0073\u02bc": phoneme(alveolar, ejective | fricative),
        "\u0283\u02bc": phoneme(postalveolar, ejective | fricative),

        "\u026c\u02bc": phoneme(alveolar, ejective | lateral | fricative),

        "\u03b2\u031e\u030a": phoneme(bilabial,approximant),
        "\u03b2\u031e": phoneme(bilabial,voiced | approximant),
        "\u028b\u0325": phoneme(labiodental,approximant),
        "\u028b": phoneme(labiodental,voiced | approximant),
        "\u00f0\u031e": phoneme(dental,voiced | approximant),
        "\u0279\u0325": phoneme(alveolar,approximant),
        "\u0279": phoneme(alveolar,voiced | approximant),
        "\u027b\u030a": phoneme(retroflex,approximant),
        "\u027b": phoneme(retroflex,voiced | approximant),
        "\u006a": phoneme(palatal,voiced | approximant),
        "\u028d": phoneme(labiovelar,approximant),
        "\u0077": phoneme(labiovelar,voiced | approximant),
        "\u0270": phoneme(velar,voiced | approximant),

        "\u006c\u0325": phoneme(alveolar,lateral | approximant),
        "\u006c": phoneme(alveolar,voiced | lateral | approximant),
        "\u026d": phoneme(retroflex,voiced | lateral | approximant),
        "\u0234": phoneme(alveolopalatal, voiced | lateral | approximant),
        "\u028e": phoneme(palatal,voiced | lateral | approximant),
        "\u029f": phoneme(velar,voiced | lateral | approximant),

        "\u0298": phoneme(bilabial, click),
        "\u01c0": phoneme(dental, click),
        "\u01c3": phoneme(alveolar, click),
        "\u01c2": phoneme(postalveolar, click),
        "\U0001df0a": phoneme(retroflex, click),
        "\u01c1": phoneme(alveolar, lateral | click),

        "\u0070\u0361\u0066": phoneme(labiodental,strident | affricate),
        "\u0062\u0361\u0076": phoneme(labiodental,strident | voiced | affricate),
        "\u0070\u0361\u0278": phoneme(bilabial,affricate),
        "\u0062\u0361\u03B2": phoneme(bilabial,voiced | affricate),
        "\u0074\u0361\u0073": phoneme(alveolar,strident | affricate),
        "\u0064\u0361\u007A": phoneme(alveolar,strident | voiced | affricate),
        "\u0074\u0361\u026C": phoneme(alveolar,lateral | affricate),
        "\u0064\u0361\u026E": phoneme(alveolar,lateral | voiced | affricate),
        "\u0074\u0361\u0283": phoneme(postalveolar,strident | affricate),
        "\u0064\u0361\u0292": phoneme(postalveolar,strident | voiced | affricate),
        "\u0074\u0361\u0255": phoneme(palatal,strident | affricate),
        "\u0064\u0361\u0291": phoneme(palatal,strident | voiced | affricate),
        "\u0288\u0361\u0282": phoneme(retroflex,strident | affricate),
        "\u0256\u0361\u0290": phoneme(retroflex,strident | affricate),
        "\u006B\u0361\u0078": phoneme(velar,affricate),
        "\u0261\u0361\u0263": phoneme(velar,voiced | affricate),
        "\u0071\u0361\u03C7": phoneme(uvular,strident | affricate),
        "\u0262\u0361\u0281": phoneme(uvular,strident | voiced | affricate),
    }
    ipa_consonant_modifiers: dict[str,phoneme_mod] = {
        "\u0325": (phoneme(0,0), ~phoneme(0,voiced)),
        "\u032c": (phoneme(0,voiced), ~phoneme(0,0)),
        "\u02b0": (phoneme(0,aspirated), ~phoneme(0,0)),
        "\u02b7": (phoneme(labialized,0),~phoneme(0,0)),
        "\u0303": (phoneme(0, nasalised), ~phoneme(0,0)),
        "\u0329": (phoneme(0, syllabic), ~phoneme(0,0)),
    }
    temp = ipa_consonants
    for (alt, mod) in zip(ipa_consonant_modifiers.keys(), ipa_consonant_modifiers.values()):
        for (sym, cons) in list(zip(ipa_consonants.keys(), ipa_consonants.values())):
            if cons.apply(mod) not in ipa_consonants.values() and cons.apply(mod) not in temp.values():
                temp[sym+alt] = cons.apply(mod)
        ipa_consonants = temp
    ipa_vowels: dict[str,phoneme] = {
        "i": phoneme(vow_high, vowel_manner),
        "y": phoneme(vow_high | vow_rounded, vowel_manner),
        "\u026f": phoneme(vow_high | vow_back, vowel_manner),
        "u": phoneme(vow_high | vow_back | vow_rounded, vowel_manner),
        "e": phoneme(vow_mid, vowel_manner),
        "\u00F8": phoneme(vow_mid | vow_rounded, vowel_manner),
        "\u0264": phoneme(vow_mid | vow_back, vowel_manner),
        "o": phoneme(vow_mid | vow_back | vow_rounded, vowel_manner),
        "a": phoneme(vow_low,vowel_manner),
        "\u0276": phoneme(vow_low | vow_rounded, vowel_manner),
        "\u0251": phoneme(vow_back | vow_low, vowel_manner),
        "\u0252": phoneme(vow_back | vow_low, vowel_manner),
    }
    ipa_vowel_modifiers: dict[str,phoneme_mod] = {
        "\u0324": (phoneme(0,vow_breathy), ~phoneme(0,0)),
        "\u0303": (phoneme(0, nasalised), ~phoneme(0,0)),
        "\u032f": (phoneme(0, 0), ~phoneme(0,syllabic)),
        "\u0330": (phoneme(0, vow_creaky), ~phoneme(0,0)),
    }
    temp = ipa_vowels
    for (alt, mod) in zip(ipa_vowel_modifiers.keys(), ipa_vowel_modifiers.values()):
        for (sym, vow) in list(zip(ipa_vowels.keys(), ipa_vowels.values())):
            if vow.apply(mod) not in ipa_vowels.values() and vow.apply(mod) not in temp.values():
                temp[sym+alt] = vow.apply(mod)
        ipa_vowels = temp
    ipa = ipa_consonants
    ipa.update(ipa_vowels)

def normalise(ph: phoneme):
    deps = {"labial": ["round"], "coronal": ["ant", "dist"], "dorsal": ["high", "low", "back", "tense"], "radical": ["atr", "rtr"]}
    deps.update({"cons": ["appx", "strid", "del_rel"], })
def group(phonemes: list[phoneme]):
    a = reduce(phoneme.__and__, phonemes)
    b = reduce(phoneme.__or__, phonemes)
    return (a, b)
def contained(phon: phoneme, phon_grp: phoneme_group):
    return (phon.apply(phon_grp) == phon)
def split_ipa(string: str) -> list[phoneme]:
    if string == "": return []
    chars = string
    split: list[str] = []
    while chars != "":
        char = ""
        possibilities = [i + 1 for i in range(len(chars)) if chars[0:i + 1] in IPA.ipa.keys()]
        if possibilities == []: raise ValueError("invalid ipa: ", string)
        char = chars[:max(possibilities)]
        split.append(char)
        chars = chars[max(possibilities):]
    return [IPA.ipa[char] for char in split]

def setrenederer():
    phoneme.renderer = IPA.ipa
def render(ph: phoneme):
    phoneme.renderer = IPA.ipa
    return str(ph)
