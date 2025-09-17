from commands import interpreter, function_form, command, command_list, command_set
import evolution_steps as evo_step
from splitter_interpreter import splitter
from vocab import Vocab
from phoneme_renderer import renderer, mod_renderer
from phoneme import phoneme

class renderer_bound_evolution:
    def __init__(self, rend: renderer, mrend: mod_renderer) -> None:
        def evo_inter_f(s: str):
            (mid, repl, pre, post) = splitter(">", "\\", "_")(s)
            begin = pre.startswith("#")
            end = post.endswith("#")
            pre = pre.removeprefix("#").strip()
            post = post.removesuffix("#").strip()
            (mid_l, repl_l, pre_l, post_l) = [mrend.split(a) for a in (mid, repl, pre, post)]
            return evo_step.evolve(pre_l, mid_l, post_l, repl_l, begin, end)
        evo_inter = interpreter(list[phoneme], list[phoneme],  evo_inter_f)
