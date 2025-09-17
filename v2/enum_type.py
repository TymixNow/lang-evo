from typing import Any, TypeVar, List, Generic
T = TypeVar('T')

class enum(Generic[T]):
    def __init__(self, l: List[T]) -> None:
        class internal:
            values = set(l)
            def __init__(self, val) -> None:
                if val is internal:
                    self = val
                elif val not in internal.values:
                    raise ValueError(val, "not in: ", list(self.values))
                else:
                    self.val = val
            def __hash__(self) -> int:
                return hash(self.val)
            def __eq__(self, other: Any) -> bool:
                match other:
                    case internal():
                        return self.val == other.val
                    case _:
                        return False
        self.t = internal
        class setfrom:
            def __init__(self, s) -> None:
                self.values = set([internal(a) for a in s])
            @classmethod
            def all(cls):
                return setfrom(l)
            @classmethod
            def none(cls):
                return setfrom([])
            def __iter__(self):
                yield from self.values
            def __add__(self, other: internal):
                v = self.values
                v.add(other)
                return setfrom(v)
        self.s = setfrom
        