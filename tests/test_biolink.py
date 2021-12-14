import unittest
from linkml_datalog.generators.dataloggen import DatalogGenerator
import os

INPUTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs')
OUTPUTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'outputs')


class DatalogGeneratorTestCase(unittest.TestCase):
    def test_gen(self):
        """
        Export Biolink Model to Datalog Schema (RDF-Based)
        :return:
        """
        fn = os.path.join(INPUTS_DIR,"biolink-model.yaml")
        print(f'Loading {fn}')
        gen = DatalogGenerator(fn)
        print(gen.serialize())
        self.assertEqual(True, True)
        with open(os.path.join(OUTPUTS_DIR,"biolink.dl"), 'w') as stream:
            stream.write(gen.serialize())




if __name__ == '__main__':
    unittest.main()
