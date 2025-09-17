from typing import Callable, TypeVar, Generic, overload
from vocab import Vocab

T_IN = TypeVar('T_IN')
T_OUT = TypeVar('T_OUT')

class interpreter(Generic[T_IN, T_OUT]):
    def __init__(self, _in: type[T_IN], _out: type[T_OUT], s: Callable[[str], Callable[[T_IN], T_OUT]]) -> None:
        self.function: Callable[[str], Callable[[T_IN], T_OUT]] = s
    def __call__(self, x: str) -> Callable[[T_IN], T_OUT]:
        return self.function(x)

class function_form(Generic[T_IN, T_OUT]):
    def __init__(self, intype: type[T_IN], outtype: type[T_OUT]) -> None:
        self.intype = intype
        self.outtype = outtype
        self.functions: dict[str, interpreter[T_IN, T_OUT]] = {}
    def __setitem__(self, s: str, c: interpreter[T_IN, T_OUT]):
        self.functions[s] = c
    def __call__(self, s: str) -> Callable[[T_IN], T_OUT]:
        m: str = max([a for a in self.functions.keys() if s.strip().startswith(a)], key=len)
        func: interpreter[T_IN, T_OUT] = self.functions[m]
        inp: str = s.strip().removeprefix(m).strip()
        return func(inp)
    def __add__(self, d: dict[str, interpreter[T_IN, T_OUT]]) -> dict[str, interpreter[T_IN, T_OUT]]:
        new = self.functions
        new.update(d)
        return new
    
class command:
    @overload
    def __init__(self, form: function_form, method: Callable[[Vocab, Callable[[T_IN], T_OUT]], Vocab]) -> None:
        self.form = form
        self.method2 = method
    @overload
    def __init__(self, form: None, method: Callable[[Vocab], Vocab]) -> None:
        self.form = None
        self.method1 = method
    def __init__(self, form, method) -> None:
        pass
    def __call__(self, vocab: Vocab, rest: str):
        match self.form:
            case None:
                return self.method1(vocab)
            case function_form():
                return self.method2(vocab, self.form(rest))
class command_set:
    def __init__(self) -> None:
        self.commands: dict[str, command] = {}
    def __setitem__(self, name: str, value: command):
        self.commands[name] = value
    def compile_line(self, line: str):
        def compiled(vocab: Vocab):
            m: str = max([a for a in self.commands.keys() if line.strip().startswith(a)], key=len)
            comm = self.commands[m]
            rest: str = line.strip().removeprefix(m).strip()
            vocab = comm(vocab, rest)
            return vocab
        return compiled
    
class command_list:
    def __init__(self, code: str, reader: command_set):
        self.code = code
        self.reader = reader
    def run(self, vocab: Vocab):
        for line in self.code.split("\n"):
            vocab = self.reader.compile_line(line)(vocab)
        return vocab


        
