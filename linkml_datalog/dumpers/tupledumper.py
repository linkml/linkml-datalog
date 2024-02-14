import logging
import os
from abc import abstractmethod
from enum import Enum
from numbers import Number
from typing import Optional, Any, Dict, List, Union
import json

from linkml_runtime.dumpers import rdflib_dumper
from rdflib import Graph, URIRef
from rdflib.term import Node, BNode, Literal, Identifier
from rdflib.namespace import RDF


from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils.schemaview import SchemaView, ElementName, PermissibleValue, PermissibleValueText
from linkml_runtime.utils.yamlutils import YAMLRoot

class Predicate(Enum):
    triple = 'triple'
    literal_number = 'literal_number'
    literal_symbol = 'literal_symbol'

    @staticmethod
    def list() -> List[str]:
        return list(map(lambda c: c.value, Predicate))


class TupleDumper(Dumper):
    """
    Dumps LinkML instance data as TSV tuples.

    Creates 3 triple files:

    - triple.facts
    - literal_number.facts
    - literal_symbol.facts

    The triples are plain RDF triples. In cases where the object is a literal,
    it will also appear in either literal_number.facts or literal_symbol.facts.
    """

    def dump(self, element: Union[YAMLRoot, Graph], schemaview: SchemaView = None, directory=None, **kwargs):
        """
        Dump a LinkML instance as TSV tuples, saving to a directory

        :param element:
        :param schemaview:
        :param directory:
        :param kwargs:
        :return:
        """
        if isinstance(element, Graph):
            g = element
        else:
            g = rdflib_dumper.as_rdf_graph(element, schemaview, **kwargs)
        self.graph_to_tuples(g, directory=directory)

    def dumps(self, *args, **kwargs) -> str:
        """
        Dump a LinkML instance as TSV tuples, returning a string
        :param args:
        :param kwargs:
        :return:
        """
        #return self.dump(*args, **kwargs)
        raise NotImplementedError

    def graph_to_tuples(self, graph: Graph, directory: str) -> None:
        """
        Convert an RDF graph Tuple format

        :param graph:
        :param directory:
        :return:
        """
        file_map = {}
        for p in Predicate.list():
            file_map[p] = open(os.path.join(directory, f'{p}.facts'), 'w')

        def safe_str(v: str) -> str:
            return str(v).replace('\t', '\\t').replace('\n', '\\n')

        def as_str(v: Identifier) -> str:
            if isinstance(v, Literal):
                v = v.toPython()
                return json.dumps(v, default=str)
                #if isinstance(v, Number) and not isinstance(v, bool):
                #    return str(v)
                #else:
                #    v = safe_str(v)
                #    return f'"{v}"'
            elif isinstance(v, BNode):
                return f'_:b{v}'
            else:
                # TODO: rdflib_dumper should treat these as literals
                if v == 'True':
                    return 'true'
                elif v == 'False':
                    return 'false'
                else:
                    return str(v)

        def emit(predicate: Predicate, *args):
            file_map[predicate.value].write('\t'.join([as_str(a) for a in args]))
            file_map[predicate.value].write('\n')

        for s, p, o in graph.triples((None, None, None)):
            emit(Predicate.triple, s, p, o)
            if isinstance(o, Literal):
                v = o.toPython()
                if isinstance(v, Number) and not isinstance(v, bool):
                    emit(Predicate.literal_number, as_str(o), v)
                else:
                    emit(Predicate.literal_symbol, as_str(o), safe_str(v))




