from enum_type import enum
from unit import unit, unit_range
from typing import Any, Optional, Union

class consonant:
    places_of_articulation = ["blb", "ldn", "llb", "den", "alv", "pav", "pal", "rtf", "vel", "uvu", "phr", "glt"]
    coarticulators =   ["", "lab", "pal", "vel", "phr"]
    manners_of_articulation = ["pls", "nas", "frc", "lfr", "afr", "laf", "tap", "trl", "apx", "lax"]
    place_of_articulation = enum[str](places_of_articulation)
    coarticulator = enum[str](coarticulators)
    manner_of_articulation = enum[str](manners_of_articulation)
    def __init__(self, place, coart, manner, syllabic: bool) -> None:
        self.place = consonant.place_of_articulation.t(place)
        self.coart = consonant.coarticulator.t(coart)
        self.manner = consonant.manner_of_articulation.t(manner)
        self.syllabic = syllabic
class consonant_kind:
    def __init__(self, place: list[str] = [], coart: list[str] = [], manner: list[str] = [], syllabic: tuple[bool, bool] = (False, False), base: list[consonant] = []) -> None:
        self.place = consonant.place_of_articulation.s(place)
        self.coart = consonant.coarticulator.s(coart)
        self.manner = consonant.manner_of_articulation.s(manner)
        self.syllabic: tuple[bool, bool] = syllabic
        for cons in base: 
            self.place.values.add(cons.place)
            self.coart.values.add(cons.coart)
            self.manner.values.add(cons.manner)
            self.syllabic = (self.syllabic[0], True) if cons.syllabic else (True, self.syllabic[1])
    def __contains__(self, other: consonant):
        return other.place in self.place and other.coart in self.coart and other.manner in self.manner
    @classmethod
    def all(cls):
        return consonant_kind(consonant.places_of_articulation, consonant.coarticulators, consonant.manners_of_articulation, (True,True))
    @classmethod
    def none(cls):
        return consonant_kind()
    def __add__(self,other: consonant | None):
        if other is None: return self
        new = self
        new.place += other.place
        new.coart += other.coart
        new.manner += other.manner
        new.syllabic =  (self.syllabic[0], True) if other.syllabic else (True, self.syllabic[1])
        return new
class consonant_mod:
    def __init__(self, place: Optional[str], coart: Optional[str], manner: Optional[str], syllabic: Optional[bool]) -> None:
        self.place = place
        self.coart = coart
        self.manner = manner
        self.syllabic = syllabic
    def __call__(self, c: consonant) -> Any:
        place = self.place if self.place is not None else c.place
        coart = self.coart if self.coart is not None else c.coart
        manner = self.manner if self.manner is not None else c.manner
        syll = self.syllabic if self.syllabic is not None else c.syllabic
        return consonant(place, coart, manner, syll)

class vowel:
    def __init__(self, frontness: unit, closeness: unit, roundness: bool, tone: unit, nasal: bool) -> None:
        self.frontness: unit = frontness
        self.closeness: unit = closeness
        self.roundness: bool = roundness
        self.tone: unit = tone
        self.nasal = nasal
class vowel_aabb:
    def __init__(self, frontness: unit_range, closeness: unit_range, roundness: tuple[bool, bool], tone: unit_range, nasal: tuple[bool, bool]) -> None:
        self.frontness: unit_range = frontness
        self.closeness: unit_range = closeness
        self.roundness: tuple[bool, bool] = roundness
        self.tone: unit_range = tone
        self.nasal = nasal
    def __contains__(self, other: vowel):
        return other.frontness in self.frontness and other.closeness in self.closeness and self.roundness[other.roundness] and other.tone in self.tone and self.nasal[other.nasal]
    @classmethod
    def none(cls):
        return vowel_aabb(unit_range.none(), unit_range.none(), (False,False), unit_range.none(), (False,False))
    @classmethod
    def all(cls):
        return vowel_aabb(unit_range.all(), unit_range.all(), (True,True), unit_range.all(), (True,True))
    def __add__(self,other: vowel | None):
        if other is None: return self
        frontness = self.frontness + other.frontness
        closeness = self.closeness + other.closeness
        roundness = (self.roundness[0], True) if other.roundness else (True, self.roundness[1])
        tone = self.tone + other.tone
        nasal = (self.nasal[0], True) if other.nasal else (True, self.nasal[1])
        return vowel_aabb(frontness, closeness, roundness, tone, nasal)
    
class vowel_mod:
    def __init__(self, frontness: Optional[unit], closeness: Optional[unit], roundness: Optional[bool], tone: Optional[unit], nasal: Optional[bool]):
        self.frontness = frontness
        self.closeness = closeness
        self.roundness = roundness
        self.tone = tone
        self.nasal = nasal
    def __call__(self, v: vowel):
        frontness = self.frontness if self.frontness is not None else v.frontness
        closeness = self.closeness if self.closeness is not None else v.closeness
        roundness = self.roundness if self.roundness is not None else v.roundness
        tone = self.tone if self.tone is not None else v.tone
        nasal = self.nasal if self.nasal is not None else v.nasal
        return vowel(frontness, closeness, roundness, tone, nasal)

class phoneme:
    def __init__(self, ph: consonant | vowel):
        match ph:
            case consonant():
                self.consonant: Optional[consonant] = ph
                self.vowel: Optional[vowel] = None
            case vowel():
                self.consonant: Optional[consonant] = None
                self.vowel: Optional[vowel] = ph
    def value(self) -> Union[consonant, vowel]:
        return self.consonant if self.consonant is not None else self.vowel # pyright: ignore[reportReturnType]
    def is_consonant(self) -> bool:
        return self.consonant is not None
    def is_vowel(self) -> bool:
        return self.vowel is not None
class phoneme_kind:
    def __init__(self, c: Optional[consonant_kind], v: Optional[vowel_aabb]):
        self.cons = c if c is not None else consonant_kind.none()
        self.vow = v if v is not None else vowel_aabb.none()
    def __contains__(self, ph: phoneme):
        if ph.is_consonant():
            return ph.consonant in self.cons  # pyright: ignore[reportOperatorIssue]
        else:
            return ph.vowel in self.vow  # pyright: ignore[reportOperatorIssue]
    @classmethod
    def all(cls):
        return phoneme_kind(consonant_kind.all(), vowel_aabb.all())
    @classmethod
    def none(cls):
        return phoneme_kind(None, None)
    @classmethod
    def group(cls, l: list[phoneme]):
        v: vowel_aabb = vowel_aabb.none()
        c: consonant_kind = consonant_kind.none()
        for ph in l:
            match ph.value():
                case vowel():
                    v += ph.vowel
                case consonant():
                    c += ph.consonant
        return phoneme_kind(c,v)

class phoneme_mod:
    def __init__(self, c: Optional[consonant_mod], v: Optional[vowel_mod]):
        self.cons = c
        self.vow = v
    def __call__(self, ph: phoneme) -> phoneme:
        if ph.is_consonant():
            return phoneme(self.cons(ph.consonant)) if self.cons is not None else ph # pyright: ignore[reportArgumentType]
        else:
            return phoneme(self.vow(ph.vowel)) if self.vow is not None else ph # pyright: ignore[reportArgumentType]
    