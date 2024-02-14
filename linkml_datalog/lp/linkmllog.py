from typing import ClassVar, Union, Iterable, Any

from snakelog.common import Vars, Var, Clause, Not
from snakelog.litelog import Solver

from linkml_datalog.lp.jsonlog import Link, RefString, Member
from linkml_datalog.pydanticlog.pydanticlog import Fact, rule, RULE


REF = Var("ref")
NAME = Var("name")
CDICT = Var("cdict")
CN = Var("cn")
SN = Var("sn")
ATT = Var("att")
VAL = Var("val")
ADICT = Var("adict")
VALREF = Var("valref")
L = Var("l")
MREF = Var("mref")
SREF = Var("sref")
U_ = Var("u")

link = Link.__rfunc__()
member = Member.__rfunc__()
ref_string = RefString.__rfunc__()

class ClassRefName(Fact):
    ref: str
    name: str

    signature: ClassVar[str] = ["class_ref_name", "TEXT", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        element_ref_name = ClassRefName.__rfunc__()
        yield (element_ref_name(REF, NAME) <= link(U_, "classes", CDICT) & link(CDICT, NAME, REF))



class SlotRefName(Fact):
    ref: str
    name: str

    signature: ClassVar[str] = ["slot_ref_name", "TEXT", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        element_ref_name = cls.__rfunc__()
        yield (element_ref_name(REF, NAME) <=
                link(U_, "slots", CDICT) & link(CDICT, NAME, REF))


class ClassInducedSlot(Fact):
    class_definition: str
    slot_name: str

    signature: ClassVar[str] = ["class_induced_slot", "TEXT", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        this = cls.__rfunc__()
        class_ref_name = ClassRefName.__rfunc__()

        yield (this(CN, SN) <=
                  link(REF, "attributes", CDICT) &
                  class_ref_name(REF, CN) &
                  link(CDICT, SN, ADICT))
        yield (this(CN, SN) <=
                  link(REF, "slots", L) &
                  member(L, U_, MREF) &
                  ref_string(MREF, SN) &
                  class_ref_name(REF, CN))

class ClassInducedSlotValueRef(Fact):
    class_definition: str
    slot_name: str
    att: str
    valref: str

    signature: ClassVar[str] = ["class_induced_slot_value_ref", "TEXT", "TEXT", "TEXT", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        classdef_slot_av = cls.__rfunc__()
        class_ref_name = ClassRefName.__rfunc__()
        slot_ref_name = SlotRefName.__rfunc__()

        yield (classdef_slot_av(CN, SN, ATT, VALREF) <=
                  link(REF, "slot_usage", CDICT) &
                  class_ref_name(REF, CN) &
                  link(CDICT, SN, ADICT) &
                  link(ADICT, ATT, VALREF))
        yield (classdef_slot_av(CN, SN, ATT, VALREF) <=
                  link(REF, "attributes", CDICT) &
                  class_ref_name(REF, CN) &
                  link(CDICT, SN, ADICT) &
                  link(ADICT, ATT, VALREF))
        yield (classdef_slot_av(CN, SN, ATT, VALREF) <=
                  link(REF, "slots", L) &
                  class_ref_name(REF, CN) &
                  member(L, U_, MREF) &
                  ref_string(MREF, SN) &
                  slot_ref_name(SREF, SN) &
                  link(SREF, ATT, VALREF))

class ClassInducedSlotValueString(Fact):
    class_definition: str
    slot_name: str
    att: str
    val: str

    signature: ClassVar[str] = ["class_induced_slot_value_string", "TEXT", "TEXT", "TEXT", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        classdef_slot_av = cls.__rfunc__()
        class_ref_name = ClassRefName.__rfunc__()
        slot_ref_name = SlotRefName.__rfunc__()

        yield (classdef_slot_av(CN, SN, ATT, VAL) <=
                  link(REF, "slot_usage", CDICT) &
                  class_ref_name(REF, CN) &
                  link(CDICT, SN, ADICT) &
                  link(ADICT, ATT, VALREF) &
                  ref_string(VALREF, VAL))
        yield (classdef_slot_av(CN, SN, ATT, VAL) <=
                  link(REF, "attributes", CDICT) &
                  class_ref_name(REF, CN) &
                  link(CDICT, SN, ADICT) &
                  link(ADICT, ATT, VALREF) &
                  ref_string(VALREF, VAL))
        yield (classdef_slot_av(CN, SN, ATT, VAL) <=
                  link(REF, "slots", L) &
                  class_ref_name(REF, CN) &
                  member(L, U_, MREF) &
                  ref_string(MREF, SN) &
                  slot_ref_name(SREF, SN) &
                  link(SREF, ATT, VALREF) &
                  ref_string(VALREF, VAL))

class PrimaryKey(Fact):
    class_definition: str
    slot_name: str

    signature: ClassVar[str] = ["primary_key", "TEXT", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        csvr = ClassInducedSlotValueRef.__rfunc__()
        this = cls.__rfunc__()
        yield this(CN, SN) <= csvr(CN, SN, "identifier", U_)


class TypeDefinition(Fact):
    element_name: str

    signature: ClassVar[str] = ["type_definition", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        element_ref_name = ClassRefName.__rfunc__()
        this = cls.__rfunc__()
        yield (this(REF) <= link(REF, "types", CDICT) & element_ref_name(CDICT, REF))
        yield this("string")  ## TODO


class AssertedRange(Fact):
    class_definition: str
    slot_name: str
    val: str

    signature: ClassVar[str] = ["asserted_range", "TEXT", "TEXT", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        csvr = ClassInducedSlotValueString.__rfunc__()
        this = cls.__rfunc__()
        yield (this(CN, SN, VAL) <= csvr(CN, SN, "range", VAL))


class HasAssertedRange(Fact):
    class_definition: str
    slot_name: str

    signature: ClassVar[str] = ["has_asserted_range", "TEXT", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        asserted_range = AssertedRange.__rfunc__()
        this = cls.__rfunc__()
        yield (this(CN, SN) <= asserted_range(CN, SN, U_))


class DefaultRange(Fact):
    val: str

    signature: ClassVar[str] = ["default_range", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        this = cls.__rfunc__()
        yield (this(VAL) <= link(U_, "default_range", REF) & ref_string(REF, VAL))


class Range(Fact):
    class_definition: str
    slot_name: str
    val: str

    signature: ClassVar[str] = ["range", "TEXT", "TEXT", "TEXT"]

    @classmethod
    def rules(cls) -> Iterable[Clause]:
        cs = ClassInducedSlot.__rfunc__()
        asserted_range = AssertedRange.__rfunc__()
        has_asserted_range = HasAssertedRange.__rfunc__()
        type_definition = TypeDefinition.__rfunc__()
        default_range = DefaultRange.__rfunc__()
        this = cls.__rfunc__()
        yield (this(CN, SN, VAL) <= asserted_range(CN, SN, VAL))
        # TODO
        yield (this(CN, SN, VAL) <= default_range(VAL) & cs(CN, SN) & Not(has_asserted_range(CN, SN)))
        #yield (this(CN, SN, VAL) <= default_range(VAL) & cs(CN, SN) & Not((type_definition(U_) & asserted_range(CN, SN, U_))))
        #yield (this(CN, SN, VAL) <= default_range(VAL) & cs(CN, SN))
