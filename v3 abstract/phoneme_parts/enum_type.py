from typing import Any, TypeVar, List, Generic, Self
from basemost.interpretable import Inter

T = TypeVar('T')

def make_enum(l: List[T]):
    class enum(metaclass = Inter):
        parts = {"val": type[T]}
        values = set(l)
        def __init__(self, val: Self | T) -> None:
            if val is enum:
                self = val
            else:
                assert val in enum.values
                self.val = val
        def __hash__(self) -> int:
            return hash(self.val)
        def __eq__(self, other: Any) -> bool:
            match other:
                case enum():
                    return self.val == other.val
                case _:
                    return False
    return enum
