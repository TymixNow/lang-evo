class splitter:
    def __init__(self, *l: str) -> None:
        self.delimiters = l
    def __call__(self, command: str) -> list[str]:
        out = []
        for delimiter in self.delimiters:
            [out[-1], command] = command.split(delimiter)
        return out