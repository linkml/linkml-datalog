import json
import os
from dataclasses import dataclass
from typing import Any

import yaml
import logging

import click
from linkml_runtime.utils.schemaview import SchemaView


from linkml_datalog.dumpers.tupledumper import TupleDumper
from linkml_datalog.generators.dataloggen import DatalogGenerator
from linkml.utils.datautils import _get_format

def runcmd(cmd: str) -> int:
    status = os.system(cmd)
    logging.info(f'{status} CMD: {cmd}')
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

    def run(self, obj: Any):
        sv = self.sv
        workdir = self.workdir
        generator = DatalogGenerator(sv.schema)
        with open(os.path.join(workdir, 'schema.dl'), 'w') as stream:
            stream.write(generator.serialize())
        generator.serialize()
        dumper = TupleDumper()
        dumper.dump(obj, sv, directory=workdir)
        runcmd(f'souffle -F{workdir} -D{workdir} {workdir}/schema.dl')



@click.command()
@click.option('--dir', '-d', required=True, help='Directory to export to')
@click.option('--schema', '-s', required=True, help='Path to schema')
@click.argument('input')
def cli(input, schema, dir):
    """
    Performs inference and validation over input files using a linkml schema

    Steps:
     - compile schema to datalog schema (schema.dl)
     - translate instance data to tuples
     - collect above in working directory
     - run souffle
    """
    logging.basicConfig(level=logging.INFO)
    sv = SchemaView(schema)
    input_format = _get_format(input)
    # TODO: compile schema
    with open(input) as stream:
        if input_format == 'yaml':
            obj = yaml.safe_load(stream)
        else:
            obj = json.load(stream)
    engine = DatalogEngine(sv, workdir=dir)
    engine.run(obj)


if __name__ == '__main__':
    cli()