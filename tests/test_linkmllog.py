from pathlib import Path
from typing import Iterable, Tuple

import pytest
import yaml
from snakelog.common import *
from snakelog.litelog import Solver, TEXT

from linkml_datalog.engines.jsonlog_engine import JsonLogEngine
from linkml_datalog.lp import jsonlog, linkmllog
from linkml_datalog.lp.jsonlog import AncestorOf, Link, RefString
from linkml_datalog.lp.linkmllog import ClassRefName, SlotRefName, ClassInducedSlotValueString, PrimaryKey, Range, \
    AssertedRange, TypeDefinition
from linkml_datalog.pydanticlog import load_module
from linkml_datalog.pydanticlog.pydanticlog import solver_print_rules

THIS = Path(__file__).parent
INPUT_DIR = THIS / "inputs"



@pytest.fixture
def solver():
    return Solver()


@pytest.fixture
def init_module(solver):
    load_module(solver, jsonlog)
    load_module(solver, linkmllog)

@pytest.fixture
def data():
    return yaml.safe_load(open(INPUT_DIR / "employee.yaml"))


def test_linkmllog(solver, init_module, data):
    jsonlog.load(solver, data)
    trules = list(ClassRefName.rules())
    print(len(trules))
    for r in trules:
        print("RULE", r)
    #assert False
    solver.run()
    results = list(ClassRefName.query(solver))
    for r in results:
        print(r)
    assert len(results) > 0
    assert ('./classes/organization', 'organization') in results
    results = list(SlotRefName.query(solver))
    for r in results:
        print(r)
    assert len(results) > 0
    assert ('./slots/employees', 'employees') in results
    print("ClassDefinitionSlotDefinition")
    results = list(ClassInducedSlotValueString.query(solver))
    for r in results:
        print(r)
    assert len(results) > 0
    assert ('employee', 'scores', 'range', 'float') in results
    assert ('person', 'id', 'pattern', '^\\S+$') in results
    assert ('person', 'category', 'is_a', 'type') in results
    results = list(PrimaryKey.query(solver))
    for r in results:
        print("PK", r)
    assert len(results) > 0
    #solver_print_rules(solver)
    results = list(AssertedRange.query(solver))
    for r in results:
        print("ASSERTED_RANGE", r)
    assert len(results) > 0
    assert ('employee', 'scores', 'float') in results
    results = list(Range.query(solver))
    for r in results:
        print("INF RANGE", r)
    assert len(results) > 0
    assert ('person', 'id', 'string') in results
    results = list(TypeDefinition.query(solver))
    for r in results:
        print("TD", r)
    assert len(results) > 0

