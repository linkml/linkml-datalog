import unittest
from pathlib import Path

import yaml
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView

import os

from linkml_datalog.dumpers.tupledumper import TupleDumper

from tests.models.personinfo import Container

INPUTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs')
OUTPUT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'outputs')

prefixes = {
    'P': 'https://example.org/P/',
    'CODE': 'https://example.org/CODE/',
    'ROR': 'https://example.org/ROR/',
    'GEO': 'https://example.org/GEO/',
}


class TupleDumperTestCase(unittest.TestCase):
    def test_tuple_dump(self):
        schema_fn = os.path.join(INPUTS_DIR, "personinfo.yaml")
        data_fn = os.path.join(INPUTS_DIR, "example_personinfo_data.yaml")
        data = yaml_loader.load(data_fn, target_class=Container)
        directory = os.path.join(OUTPUT_DIR, 'persondata')
        Path(directory).mkdir(exist_ok=True)
        with open(data_fn) as stream:
            obj = yaml.safe_load(stream)
        sv = SchemaView(schema_fn)
        tuple_dumper = TupleDumper()
        tuple_dumper.dump(data, schemaview=sv, prefix_map=prefixes, directory=directory)


if __name__ == '__main__':
    unittest.main()
