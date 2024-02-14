import unittest
from pathlib import Path
from typing import Type, Tuple, List

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView

import os

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import ConjunctiveGraph, RDF, Namespace, URIRef, RDFS

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
    """
    Tests end-to-end compilation to datalog and execution.
    """

    def test_engine(self):
        """
        End-to-end test of the datalog engine.

        Compiles a standard personinfo schema and data and runs the engine.
        Uses example_personinfo_data, this is expected to have validation errors.
        """
        schema_fn = os.path.join(INPUTS_DIR, "personinfo.yaml")
        data_fn = os.path.join(INPUTS_DIR, "example_personinfo_data.yaml")
        data: Container = yaml_loader.load(data_fn, target_class=Container)
        directory = os.path.join(OUTPUT_DIR, 'persondata')
        Path(directory).mkdir(exist_ok=True)
        sv = SchemaView(schema_fn)
        e = DatalogEngine(sv, workdir=os.path.join(OUTPUT_DIR, 'tmp'))
        e.run(data, prefix_map=prefixes)
        rpt = e.validation_results()
        assert len(rpt.results) > 1
        #for result in rpt.results:
        #    print(f' * {result}')
        def has_type(t):
            matches = [result for result in rpt.results if result.type == t]
            return matches != []
        assert len(rpt.results) > 0
        assert has_type('sh:MaxInclusiveConstraintComponent')

        self._check_tuples(e, Person, personinfo.slots.grandfather_of, expected=1)
        self._check_tuples(e, Person, personinfo.slots.sibling_of,
                           min_expected=3,
                           contains=[('https://example.org/P/002', 'https://example.org/P/001'),
                                     ('https://example.org/P/003', 'https://example.org/P/003'),
                                     ])
        self._check_tuples(e, Person, personinfo.slots.ancestor_of,
                           min_expected=3,
                           contains=[('https://example.org/P/005', 'https://example.org/P/004'),
                                     ('https://example.org/P/005', 'https://example.org/P/001'),
                                     ])
        self._check_tuples(e, Person, personinfo.slots.age_category,
                           min_expected=3,
                           contains=[('https://example.org/P/001', 'http://purl.obolibrary.org/obo/HsapDv_0000087'),
                                     ('https://example.org/P/006', 'http://purl.obolibrary.org/obo/HsapDv_0000086'),
                                     ])
        e.materialize_inferences(data)
        ys = yaml_dumper.dumps(data)
        print(ys)
        p1 = next(p for p in data.persons if p.id == 'P:001')
        p4 = next(p for p in data.persons if p.id == 'P:004')
        p5 = next(p for p in data.persons if p.id == 'P:005')
        self.assertCountEqual(p5.ancestor_of, [p1.id, p4.id])

    def test_engine_rdf(self):
        """uses a collection of annotated named graphs as test  """
        schema_fn = os.path.join(INPUTS_DIR, "personinfo.yaml")
        sv = SchemaView(schema_fn)

        LINKML = Namespace('https://w3id.org/linkml/')
        g = ConjunctiveGraph()
        g.parse(os.path.join(INPUTS_DIR, "instance_tests.trig"), format='trig')
        for subg in g.contexts():
            subg_id = subg.identifier
            print(f'EVALUATING: {URIRef(subg.identifier)} -- {subg}')
            typs = list(g.objects(subject=subg_id, predicate=RDF.type))
            if LINKML.TestGraph not in typs:
                print(f' SKIPPING: {subg}')
                continue
            for cmt in g.objects(subject=subg_id, predicate=RDFS.comment):
                print(f'## {cmt}')
            directory = os.path.join(OUTPUT_DIR, 'persondata')
            Path(directory).mkdir(exist_ok=True)
            e = DatalogEngine(sv, workdir=os.path.join(OUTPUT_DIR, 'tmp'))
            e.run(subg, prefix_map=prefixes)
            rpt = e.validation_results()
            print(f' RESUlTS: {subg} = {len(rpt.results)}')
            for result in rpt.results:
                print(f' * {result}')
            def has_type(t):
                matches = [result for result in rpt.results if result.type == t]
                print(f'MATCHES({t}) = {matches}')
                return matches != []
            expected_fails = list(g.objects(subject=subg_id, predicate=LINKML.fail))
            for e in expected_fails:
                e_curie = e.n3(g.namespace_manager)
                assert has_type(e_curie)
            for v in g.objects(subject=subg_id, predicate=LINKML.max_validation_results):
                max_results = v.value
                print(f' MAX RESULTS EXPECTED; testing if {len(rpt.results)} <= {max_results} // {type(v)}')
                self.assertLessEqual(len(rpt.results), max_results)
            print('PASSES')


    def _check_tuples(self, e: DatalogEngine, cls: Type[YAMLRoot], slot: Slot, min_expected=1, max_expected=100,
                      expected=None, contains: List[Tuple[str, str]] = None):
        tups = e.inferred_slot_values(cls.class_name, slot.name)
        for t in tups:
            print(f'  T({cls} {slot}) = {t}')
        if expected is not None:
            min_expected = expected
            max_expected = expected
        if min_expected is not None:
            self.assertGreaterEqual(len(tups), min_expected)
        if max_expected is not None:
            self.assertLessEqual(len(tups), max_expected)
        if contains:
            for c in contains:
                self.assertIn(c, tups)


if __name__ == '__main__':
    unittest.main()
