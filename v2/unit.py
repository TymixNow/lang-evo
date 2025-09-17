class unit:
    def __init__(self, value: float) -> None:
        self.value = max(0,min(int(value*255), 255))
    def __lt__(self, other) -> bool:
        return self.value < other.value
    def __gt__(self, other) -> bool:
        return other < self
    def __le__(self, other) -> bool:
        return not (other < self)
    def __ge__(self, other) -> bool:
        return not (other > self)
    def __eq__(self, other) -> bool:
        return self.value == other.value
    def __neq__(self, other) -> bool:
        return not self == other
    def __float__(self):
        return (float(self.value) / 255.0)
    def __str__(self):
        return str(float(self.value) / 255.0)

class unit_range:
    def __init__(self, *args: unit, empty = False) -> None:
        if empty:
            self.min = unit(1.0)
            self.max = unit(0.0)
        else:
            self.max = max(*args)
            self.min = min(*args)
    def __contains__(self, *args: unit):
        return all([a >= self.min and a <= self.max for a in args])
    def __add__(self, *args: unit):
        out = self
        for arg in args: 
            out.min = min(out.min, arg.value)
            out.max = max(out.max, arg.value)
        return out
    def __iadd__(self, *args: unit):
        for arg in args:
            self = self + arg

    @classmethod
    def all(cls):
        return unit_range(unit(0.0), unit(1.0))
    @classmethod
    def none(cls):
        return unit_range(empty=True)
