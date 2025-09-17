from typing import Generic, TypeVar, Callable

C = TypeVar('C')

class kind(Generic[C]):
    def __init__(self, cl: Callable[[C], bool]) -> None:
        self.data = cl
    def __contains__(self, obj: C) -> bool:
        return self.data(obj)
    @classmethod
    def all(cls):
        kind[C](lambda _: True)
    @classmethod
    def none(cls):
        kind[C](lambda _: False)

class mod(Generic[C]):
    def __init__(self, cl: Callable[[C], C]) -> None:
        self.data = cl
    def __call__(self, obj: C) -> C:
        return self.data(obj)

