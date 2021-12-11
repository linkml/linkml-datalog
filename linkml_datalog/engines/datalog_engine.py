import csv
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Union, Tuple

import yaml
import logging

import click
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinitionName
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.schemaview import SchemaView, ClassDefinitionName
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import Graph

from linkml_datalog.dumpers.tupledumper import TupleDumper
from linkml_datalog.generators.dataloggen import DatalogGenerator
from linkml.utils.datautils import _get_format, infer_root_class, get_loader, dumpers_loaders
from linkml_datalog.model.validation import ValidationReport, ValidationResult


def runcmd(cmd: str) -> int:
    status = os.system(cmd)
    logging.info(f'{status} CMD: {cmd}')
    if status != 0:
        raise Exception(f'Error running" {cmd}')
    return status

@dataclass
class DatalogEngine:
    """
    Engine for performing datalog operations on linkml data

    ALPHA

    uses DatalogDumper

    """
    sv: SchemaView = None
    workdir: str = None

    def run(self, obj: Union[YAMLRoot, Graph], prefix_map: Dict[str, str] = None):
        """
        Run datalog inference over a data object
        """
        sv = self.sv
        workdir = self.workdir
        generator = DatalogGenerator(sv.schema)
        with open(os.path.join(workdir, 'schema.dl'), 'w') as stream:
            stream.write(generator.serialize())
        generator.serialize()
        dumper = TupleDumper()
        dumper.dump(obj, sv, directory=workdir, prefix_map=prefix_map)
        runcmd(f'souffle -F{workdir} -D{workdir} {workdir}/schema.dl')

    def _parse_results(self, pred: str) -> List[List[str]]:
        with open(os.path.join(self.workdir, f'{pred}.csv')) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            return [row for row in reader]

    def validation_results(self) -> ValidationReport:
        """
        Retrieves validation results, after running souffle
        """
        rows = self._parse_results('validation_result')
        results = []
        for [typ, subject, cls, pred, val, info] in rows:
            result = ValidationResult(type=typ,
                                      subject=subject,
                                      instantiates=cls,
                                      predicate=pred,
                                      object_str=val,
                                      info=info)
            results.append(result)
        return ValidationReport(results=results)

    def inferred_slot_values(self, cn: ClassDefinitionName, sn: SlotDefinitionName) -> List[Tuple[str, str]]:
        return [tuple(r) for r in self._parse_results(f'{cn}_{sn}')]









@click.command()
@click.option('--dir', '-d', required=True, help='Directory to export to')
@click.option('--schema', '-s', required=True, help='Path to schema')
@click.option("--input-format", "-f",
              type=click.Choice(list(dumpers_loaders.keys())),
              help="Input format. Inferred from input suffix if not specified")
@click.option("--target-class", "-C",
              help="name of class in datamodel that the root node instantiates")
@click.option("--module", "-m",
              help="Path to python datamodel module")
@click.argument('input')
def cli(input, schema, module, target_class, input_format, dir):
    """
    Performs inference and validation over input files using a linkml schema

    Steps:
     - compile schema to datalog schema (schema.dl)
     - translate instance data to tuples
     - collect above in working directory
     - run souffle
    """
    logging.basicConfig(level=logging.INFO)
    if module is None:
        if schema is None:
            raise Exception('must pass one of module OR schema')
        else:
            python_module = PythonGenerator(schema).compile_module()
    else:
        python_module = compile_python(module)
    sv = SchemaView(schema)
    input_format = _get_format(input, input_format)
    loader = get_loader(input_format)
    if target_class is None:
        target_class = infer_root_class(sv)
    if target_class is None:
        raise Exception(f'target class not specified and could not be inferred')
    py_target_class = python_module.__dict__[target_class]

    obj = loader.load(source=input,  target_class=py_target_class)
    engine = DatalogEngine(sv, workdir=dir)
    engine.run(obj)
    rpt = engine.validation_results()
    print(yaml_dumper.dumps(rpt))


if __name__ == '__main__':
    cli()