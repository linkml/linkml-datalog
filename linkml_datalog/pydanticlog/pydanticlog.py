import json
from types import ModuleType
from typing import ClassVar, Optional, Union, Type, Callable, Iterable, Tuple, List

from pydantic import BaseModel
from snakelog.common import Atom, Var, Clause
from snakelog.litelog import Solver


RULE = Tuple[Atom, List[Atom]]

class Fact(BaseModel):
    """
    Base class for all Fact models
    """
    predicate_name: ClassVar[Optional[str]] = None
    signature: ClassVar[str] = []

    @classmethod
    def get_signature(cls):
        return cls.signature

    @classmethod
    def __relation__(cls, solver: Solver) -> Callable:
        sig = cls.get_signature()
        return solver.Relation(*sig)

    @classmethod
    def predicate(cls) -> str:
        sig = cls.get_signature()
        return sig[0]

    @classmethod
    def __rfunc__(cls) -> Callable[..., Atom]:
        return lambda *args: Atom(cls.predicate(), args)

    @classmethod
    def query(cls, solver: Solver, **kwargs):
        return query(solver, cls, **kwargs)

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        pass


def rule(func):
    """
    Decorator to mark a function as a rule

    :param func:
    :return:
    """
    func.is_rule = True
    return func


def load_module(solver: Solver, module: Optional[ModuleType] = None):
    if module is None:
        module = globals()
    # iterate over all classes in the module
    for c in module.__dict__.values():
        if isinstance(c, type) and issubclass(c, Fact):
            sig = c.get_signature()
            if sig:
                solver.Relation(*sig)
            rules = c.rules()
            if rules:
                for r in rules:
                    solver.add(r)
    # iterate over all functions in the module, find ones decorated as rules
    for f in module.__dict__.values():
        if hasattr(f, 'is_rule'):
            f(solver)


def query(solver: Solver, predicate: Optional[Union[str, Type]] = None, run=False):
    """
    Infer facts from the JSON documents

    :param predicate:
    :return:
    """
    if run:
        solver.run()
    if isinstance(predicate, Type):
        # test if the class is a subclass of Fact
        if issubclass(predicate, Fact):
            sig = predicate.get_signature()
            predicate = sig[0]
        else:
            predicate = predicate.__name__
    solver.cur.execute(f"SELECT * FROM {predicate}")
    return solver.cur.fetchall()


def solver_print_rules(solver: Solver):
    for rule in solver.rules:
        if rule[1]:
            print(as_prolog(rule))

def as_prolog(rule):
    head, body = rule
    argstr = ',\n  '.join([as_prolog_atom(b) for b in body])
    return f"{as_prolog_atom(head)} :-\n  {argstr}."


def as_prolog_atom(atom: Atom):
    return f"{atom.name}({', '.join([as_prolog_arg(a) for a in atom.args])})"


def as_prolog_arg(arg):
    if isinstance(arg, Var):
        return str(arg.name).upper()
    else:
        return json.dumps(arg)
