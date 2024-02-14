import json
from typing import ClassVar, Union, List, Any, Iterable

import yaml
from snakelog.common import Vars, Atom, Clause, Var
from snakelog.litelog import Solver

from linkml_datalog.dumpers.jsonfactsdumper import object_to_tuples
from linkml_datalog.pydanticlog.pydanticlog import Fact, rule


REF = Var("ref")
VAL = Var("val")

class RefPath(Fact):
    """
    A path to a reference
    """
    signature: ClassVar[str] = ["path", "TEXT", "TEXT"]

    ref: str
    path: str


class Link(Fact):
    """
    A slot and its value
    """
    signature: ClassVar[str] = ["sv", "TEXT", "TEXT", "TEXT"]

    ref: str
    att: str
    value: str


class Member(Fact):
    """
    A member of a list
    """
    signature: ClassVar[str] = ["nth", "TEXT", "INTEGER", "TEXT"]

    ref: str
    offset: int
    value: str


class RefNumber(Fact):
    """
    A reference to a number
    """
    signature: ClassVar[str] = ["literal_number", "TEXT", "NUMBER"]

    ref: str
    value: Union[int, float]


class RefBoolean(Fact):
    """
    A reference to a number
    """
    signature: ClassVar[str] = ["literal_boolean", "TEXT", "BOOLEAN"]

    ref: str
    value: bool


class RefString(Fact):
    """
    A reference to a string
    """
    signature: ClassVar[str] = ["literal_string", "TEXT", "TEXT"]

    ref: str
    value: str


class RefNull(Fact):
    """
    A reference to a null
    """
    signature: ClassVar[str] = ["literal_null", "TEXT"]

    ref: str


class RefValue(Fact):
    """
    A reference to a value (any type)
    """
    signature: ClassVar[str] = ["ref_value", "TEXT", "TEXT", "TEXT", "NUMBER", "BOOLEAN"]
    ref: Any
    datatype: str
    value_str: str
    value_number: Union[int, float]
    value_boolean: bool

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        this = cls.__rfunc__()
        ref_string = RefString.__rfunc__()
        ref_number = RefNumber.__rfunc__()
        ref_boolean = RefBoolean.__rfunc__()
        ref_null = RefNull.__rfunc__()
        yield (this(REF, "string", VAL, 0, False) <= ref_string(REF, VAL))
        yield (this(REF, "number", "", VAL, False) <= ref_number(REF, VAL))
        yield (this(REF, "boolean", "", 0, VAL) <= ref_boolean(REF, VAL))
        yield (this(REF, "null", "", 0, False) <= ref_null(REF, VAL))



class AncestorOf(Fact):
    """
    Entailed fact
    """
    ancestor: str
    descendant: str

    signature: ClassVar[str] = ["ancestor_of", "TEXT", "TEXT"]


def load(solver: Solver, sources: Union[str, List[str]]):
    """
    Load JSON documents into the solves.

    :param sources:
    :return:
    """
    if not isinstance(sources, list):
        sources = [sources]
    for source in sources:
        if not isinstance(source, str):
            doc = source
        elif source.endswith(".json"):
            doc = json.load(open(source))
        elif source.endswith(".yaml"):
            doc = yaml.safe_load(open(source))
        else:
            doc = json.loads(source)
        fact_iter = object_to_tuples(doc)
        for fact in fact_iter:
            atom = Atom(fact[0].value, fact[1])
            solver.add(atom)



@rule
def json_rules(s: Solver):
    x, y, z, u_ = Vars("x y z u")
    link = Link.__relation__(s)
    ancestor_of = AncestorOf.__relation__(s)
    s.add(ancestor_of(x, y) <= link(x, u_, y))
    s.add(ancestor_of(x, y) <= ancestor_of(x, z) & ancestor_of(z, y))
