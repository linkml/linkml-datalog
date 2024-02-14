from typing import Iterable, Tuple

import pytest
from snakelog.common import *
from snakelog.litelog import Solver, TEXT

from linkml_datalog.engines.jsonlog_engine import JsonLogEngine
from linkml_datalog.lp.jsonlog import AncestorOf, RefValue


@pytest.fixture
def solver():
    return Solver()


@pytest.fixture
def engine():
    return JsonLogEngine()


@pytest.fixture
def data():
    return {
        "persons": {
            "p1": {
                "name": "Alice",
                "age": 25,
                "aliases": ["A", "Ally"],
                "address": None,
                "alive": True,
            },
        },
    }

def test_jsonlog(solver, engine, data):
    engine.load(data)
    #results = list(engine.infer(AncestorOf))
    results = list(AncestorOf.query(engine.solver, run=True))
    for r in results:
        print(r)
    assert len(results) > 0
    assert ('.', './persons/p1/aliases') in results
    results = list(RefValue.query(engine.solver, run=False))
    for r in results:
        print("RV", r)
    assert len(results) > 0
    #assert ('.', './persons/p1/aliases') in results

