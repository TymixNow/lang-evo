from typing import Callable, Any

class Inter(type):
    methods: dict[type, Callable[[str], dict[str, str]]] = {}
    mappings: dict[type, Callable] = {}
    @classmethod
    def map_type(cls, t: type):
        if isinstance(t, Inter):
            return t.interpret
        else:
            return Inter.mappings[t]
    @property 
    def method(cls) -> Callable[[str], dict[str, str]]: 
        try:
            return Inter.methods[cls]
        finally:
            return lambda _: {}
    @method.setter
    def method(cls, c: Callable[[str], dict[str, str]]):
        Inter.methods[cls] = c
    @classmethod
    def add_mapping(cls, t: type, c: Callable[[str], Any]):
        Inter.mappings[t] = c
    @property
    def parts(cls) -> dict[str, type]:
        return {}
    def __make__(cls, **conv):
        return cls(**conv)
    def interpret(cls, s: str) -> Callable[[str], Any]: 
        data = cls.method(s)
        conv: dict[str, Any] = {}
        for name in cls.parts:
            conv[name] = Inter.map_type(cls.parts[name])(data[name])
        return cls.__make__(**conv)
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        assert "interpreter" not in attrs
        assert "parts" in attrs and type(attrs["parts"]) == dict[str, type]
        assert "__make__" in attrs and callable(attrs["__make__"])
        return super().__new__(cls, name, bases, attrs)