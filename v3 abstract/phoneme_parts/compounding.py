from typing import Any
from basemost.interpretable import Inter


def Struct(**types: type):
    class struct(metaclass = Inter):
        parts = types
        def __init__(self, **data) -> None:
            for key in types:
                setattr(self, key, data[key])
    return struct

def Union(*types: type):
    class union(metaclass = Inter):
        parts = {"data": Any}
        @classmethod
        def __make__(cls, data: Any):
            assert type(data) in types
            return union(data)
        def __init__(self, data):
            self.t: type
            self.v: Any
            if type(data) in types:
                self.t = type(data)
                self.v = data
            else:
                raise TypeError(type(data).__name__, ", the type of: ", data, "is not one of allowed types in union: ", [a.__name__ for a in types])
    return union
