import unittest
from linkml_datalog.generators.dataloggen import DatalogGenerator
import os

INPUTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs')


class DatalogGeneratorTestCase(unittest.TestCase):
    def test_gen(self):
        fn = os.path.join(INPUTS_DIR, "personinfo.yaml")
        print(f'Loading {fn}')
        gen = DatalogGenerator(fn)
        print(gen.serialize())
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
