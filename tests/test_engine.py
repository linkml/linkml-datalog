import unittest
from pathlib import Path
from typing import Type

import yaml
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView

import os

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml_datalog.dumpers.tupledumper import TupleDumper
from linkml_datalog.engines.datalog_engine import DatalogEngine

from tests.models.personinfo import Container, Person
import tests.models.personinfo as personinfo

INPUTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs')
OUTPUT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'outputs')

prefixes = {
    'P': 'https://example.org/P/',
    'CODE': 'https://example.org/CODE/',
    'ROR': 'https://example.org/ROR/',
    'GEO': 'https://example.org/GEO/',
}


class DatalogEngineTestCase(unittest.TestCase):

    def test_engine(self):
        """tests souffle engine"""
        schema_fn = os.path.join(INPUTS_DIR, "personinfo.yaml")
        data_fn = os.path.join(INPUTS_DIR, "example_personinfo_data.yaml")
        data = yaml_loader.load(data_fn, target_class=Container)
        directory = os.path.join(OUTPUT_DIR, 'persondata')
        Path(directory).mkdir(exist_ok=True)
        with open(data_fn) as stream:
            obj = yaml.safe_load(stream)
        sv = SchemaView(schema_fn)
        tuple_dumper = TupleDumper()
        #tuple_dumper.dump(data, schemaview=sv, prefix_map=prefixes, directory=directory)
        e = DatalogEngine(sv, workdir=os.path.join(OUTPUT_DIR, 'tmp'))
        e.run(data, prefix_map=prefixes)
        rpt = e.validation_results()
        #print(rpt)
        for result in rpt.results:
            print(f' * {result}')
        self._check_tuples(e, Person, personinfo.slots.grandfather_of, expected=1)

    def _check_tuples(self, e: DatalogEngine, cls: Type[YAMLRoot], slot: Slot, min_expected=1, max_expected=100, expected=None):
        tups = e.inferred_slot_values(cls.class_name, slot.name)
        for t in tups:
            print(f'  T({cls} {slot}) = {t}')
        if expected is not None:
            min_expected = expected
            max_expected = expected
        if min_expected is not None:
            self.assertLessEqual(len(tups), min_expected)
        if max_expected is not None:
            self.assertGreaterEqual(len(tups), max_expected)


if __name__ == '__main__':
    unittest.main()
