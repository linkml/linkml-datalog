import json
from dataclasses import dataclass, field
from typing import Union, List, Optional, Type

import yaml

import linkml_datalog.pydanticlog.pydanticlog
from linkml_datalog.pydanticlog import pydanticlog
from linkml_datalog.pydanticlog.pydanticlog import Fact
from linkml_datalog.dumpers.jsonfactsdumper import object_to_tuples
import linkml_datalog.lp.jsonlog as jsonlog

from snakelog.common import *
from snakelog.litelog import Solver, TEXT

def print_schema(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in cursor.fetchall():
        print(f'\nTable name: {table[0]}')
        cursor.execute(f"PRAGMA table_info({table[0]})")
        print("Column_Info:")
        print(f"{'CID':<5}{'Name':<15}{'Type':<10}{'Notnull':<10}{'Dflt_value':<15}{'Pk':<5}")
        for row in cursor.fetchall():
            print(row)


@dataclass
class JsonLogEngine:
    """
    An engine that reasons over JSON documents
    """
    solver: Solver = field(default_factory=Solver)

    def __post_init__(self):
        linkml_datalog.pydanticlog.pydanticlog.load_module(self.solver, jsonlog)


    def infer(self, predicate: Optional[Union[str, Type]] = None):
        """
        Infer facts from the JSON documents

        :param predicate:
        :return:
        """
        return pydanticlog.query(self.solver, predicate, run=True)

    def load(self, sources: Union[str, List[str]]):
        """
        Load JSON documents into the engine.

        >>> engine = JsonLogEngine()
        >>> engine.load('tests/inputs/minimal.yaml')

        :param sources:
        :return:
        """
        jsonlog.load(self.solver, sources)

