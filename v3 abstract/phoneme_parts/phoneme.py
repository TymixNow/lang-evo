from compounding import Struct, Union
from enum_type import make_enum
from unit import unit
from utils.splitter_interpreter import splitter
from basemost.interpretable import Inter

def user_friendly_boolean_interpreter(s: str):
    truthy = set("yt1")
    falsey = set("nf0")
    if s.lower()[0] in truthy: return True
    if s.lower()[0] in falsey: return False
    else: return user_friendly_boolean_interpreter(input(f"is {s} truthy? y/n >"))


class phonetics:
    places_of_articulation = make_enum(["blb", "ldn", "llb", "den", "alv", "pav", "pal", "rtf", "vel", "uvu", "phr", "glt"])
    coarticulators = make_enum(["", "lab", "pal", "vel", "phr"])
    manners_of_articulation = make_enum(["pls", "nas", "frc", "lfr", "afr", "laf", "tap", "trl", "apx", "lax"])
    consonant = Struct(place=places_of_articulation, coart=coarticulators, manner=manners_of_articulation, syllabic=bool)
    vowel = Struct(frontness=unit, closeness=unit, roundness=bool, tone=unit, nasal=bool)
    Phoneme = Union(consonant, vowel)

    unit.method = lambda x: {"value": x}
    places_of_articulation.method = lambda x: {"val": x}
    coarticulators.method = lambda x: {"val": x}
    manners_of_articulation.method = lambda x: {"val": x}
    consonant.method = lambda code: dict(zip(["place", "coart", "manner", "syllabic"],splitter("p:", "c:", "m:", "s:")(code)))
    vowel.method = lambda code: dict(zip(["frontness", "closeness", "roundness", "tone", "nasal"], splitter("f:", "c:", "r:", "t:", "n:")(code)))
    Inter.add_mapping(float, float)
    Inter.add_mapping(str, lambda x:x)
    Inter.add_mapping(bool, user_friendly_boolean_interpreter)
