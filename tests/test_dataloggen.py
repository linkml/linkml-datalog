import unittest
from linkml_datalog.generators.dataloggen import DatalogGenerator
import os

INPUTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs')
OUTPUTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'outputs')


BIOLINK_LINES = [
    ".decl Gene(i: symbol)",
    ".decl Gene_asserted(i: identifier)",
    ".output Gene",
    'Gene_asserted(i) :- triple(i, RDF_TYPE, "https://w3id.org/biolink/vocab/Gene").',
    "Gene(i) :- Gene_asserted(i).",
]

class DatalogGeneratorTestCase(unittest.TestCase):
    """
    Tests the output of the DatalogGenerator.

    TODO: Avoid TestByGuru
    """
    def test_gen(self):
        fn = os.path.join(INPUTS_DIR, "personinfo.yaml")
        print(f'Loading {fn}')
        gen = DatalogGenerator(fn)
        prog = gen.serialize()
        print(prog)
        assert ".decl name(i: identifier, v: identifier)" in prog

    def test_biolink(self):
        fn = os.path.join(INPUTS_DIR, "biolink-model.yaml")
        print(f'Loading {fn}')
        gen = DatalogGenerator(fn)
        prog = gen.serialize()
        with open(os.path.join(OUTPUTS_DIR, 'biolink.dl'), 'w') as stream:
            stream.write(prog)
        for line in BIOLINK_LINES:
            assert line in prog


if __name__ == '__main__':
    unittest.main()
