from basemost.interpretable import Inter

class unit(metaclass = Inter):
    parts = {"value": float}
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
