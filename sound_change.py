from evolution_steps import evolve_leq, metathesise, epenthesise
from typing import Callable
from ipa import phoneme, group, split_ipa
from functools import reduce

def combine_funclist(funclist: list[Callable]):
    def combine(func1, func2):
        def combined(input):
            return func1(func2(input))
        return combined
    return reduce(combine, funclist, lambda a:a)

def read_sound_change(code: str) -> tuple[list[Callable[[list[phoneme]], list[phoneme]]], list[tuple[str, list[str] | None] | None]]:
    calls = {"```": "none", "MET": "metath", "EVO": "evolve", "EPE": "epenth", "GRM": "addgrm"}
    funcs: list[Callable[[list[phoneme]], list[phoneme]]] = []
    grammar_changes: list[tuple[str, list[str] | None] | None] = []
    curr_func = "none"
    for line in code.split("\n"):
        if any(line.startswith(a) for a in calls.keys()):
            curr_func = calls[line[0:3]]
            continue
        match curr_func:
            case "evolve":
                [mid_s, rest] = line.split(">",1)
                [repl_s, rest] = rest.split("\\",1)
                [pre_s, rest] = rest.split("_", 1)
                [post_s, _] = rest.split(";", 1)
                (mid_s, repl_s, pre_s, post_s) = (a.strip() for a in (mid_s,repl_s,pre_s,post_s))
                begin = pre_s.startswith("#")
                pre_s = pre_s.removeprefix("#")
                end = post_s.endswith("#")
                post_s = post_s.removesuffix("#")
                (mid_l, pre_l, post_l) = ([gr.strip() for gr in part.split("|")] for part in (mid_s,pre_s,post_s))
                (mid_l, pre_l, post_l) = (a if a != [""] else [] for a in (mid_l, pre_l, post_l))
                (mid,pre,post) = tuple(([group(split_ipa(gr)) for gr in l] for l in (mid_l, pre_l, post_l)))
                repl = [group(split_ipa(gr.strip())) if gr.strip != "" else None for gr in repl_s.split("|")]
                funcs.append(evolve_leq(pre,mid,post,repl,begin,end))
                grammar_changes.append(None)
            case "metath":
                [first_s, rest] = line.split("<>",1)
                [second_s, rest] = rest.split("\\",1)
                [pre_s, rest] = rest.split("_", 1)
                [post_s, comm] = rest.split(";", 1)
                (first_s,second_s, pre_s, post_s) = (a.strip() for a in (first_s,second_s,pre_s,post_s))
                begin = pre_s.startswith("#")
                pre_s = pre_s.removeprefix("#")
                end = post_s.endswith("#")
                post_s = post_s.removesuffix("#")
                (first_l,second_l, pre_l, post_l) = ([gr.strip() for gr in part.split("|")] for part in (first_s,second_s,pre_s,post_s))
                (first_l,second_l, pre_l, post_l) = (a if a != [""] else [] for a in (first_l,second_l, pre_l, post_l))
                (first,second,pre,post) = tuple(([group(split_ipa(gr)) for gr in l] for l in (first_l, second_l, pre_l, post_l)))
                funcs.append(metathesise(pre,first,second,post,begin,end))
                grammar_changes.append(None)
            case "epenth":
                [_, rest] = line.split(">",1)
                [insert_s, rest] = rest.split("\\",1)
                [pre_s, rest] = rest.split("_", 1)
                [post_s, comm] = rest.split(";", 1)
                (insert_s, pre_s, post_s) = (a.strip() for a in (insert_s,pre_s,post_s))
                begin = pre_s.startswith("#")
                pre_s = pre_s.removeprefix("#")
                end = post_s.endswith("#")
                post_s = post_s.removesuffix("#")
                ( pre_l, post_l) = ([gr.strip() for gr in part.split("|")] for part in (pre_s,post_s))
                (pre_l, post_l) = (a if a != [""] else [] for a in ( pre_l, post_l))
                insert = split_ipa(insert_s)
                (pre,post) = tuple(([group(split_ipa(gr)) for gr in l] for l in (pre_l, post_l)))
                funcs.append(epenthesise(pre, insert, post, begin, end))
                grammar_changes.append(None)
            case "addgrm":
                [new_col_name_s, rest] = line.split(":",1)
                [insert_s, rest] = rest.split("\\",1)
                [pre_s, rest] = rest.split("_", 1)
                [post_s, old_col_names_s] = rest.split(";", 1)

                (insert_s, pre_s, post_s) = (a.strip() for a in (insert_s,pre_s,post_s))
                begin = pre_s.startswith("#")
                pre_s = pre_s.removeprefix("#")
                end = post_s.endswith("#")
                post_s = post_s.removesuffix("#")
                ( pre_l, post_l) = ([gr.strip() for gr in part.split("|")] for part in (pre_s,post_s))
                (pre_l, post_l) = (a if a != [""] else [] for a in ( pre_l, post_l))
                insert = split_ipa(insert_s)
                (pre,post) = tuple(([group(split_ipa(gr)) for gr in l] for l in (pre_l, post_l)))
                funcs.append(epenthesise(pre, insert, post, begin, end))

                if old_col_names_s.strip() == "":
                    old_col_names = None
                else:
                    old_col_names = [a.strip() for a in old_col_names_s.split(",")]
                new_col_name = new_col_name_s.strip()
                grammar_changes.append((new_col_name,old_col_names))
            case _:
                pass
    return (funcs, grammar_changes)
