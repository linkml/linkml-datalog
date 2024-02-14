import logging
import os
from abc import abstractmethod
from enum import Enum
from functools import lru_cache
from numbers import Number
from pathlib import Path
from typing import Optional, Any, Dict, List, Union, TextIO, Iterator, Tuple, Iterable, ClassVar, Callable
import json

from linkml_runtime.dumpers import rdflib_dumper, yaml_dumper
from pydantic import BaseModel
from rdflib import Graph, URIRef
from rdflib.term import Node, BNode, Literal, Identifier
from rdflib.namespace import RDF


from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils.schemaview import SchemaView, ElementName, PermissibleValue, PermissibleValueText
from linkml_runtime.utils.yamlutils import YAMLRoot


class Predicate(Enum):
    PATH = 'path'
    SV = 'sv'
    NTH = 'nth'
    LITERAL_NUMBER = 'literal_number'
    LITERAL_BOOLEAN = 'literal_boolean'
    LITERAL_STRING = 'literal_string'
    LITERAL_NULL = 'literal_null'

    @staticmethod
    def list() -> List[str]:
        return list(map(lambda c: c.value, Predicate))

# TODO: replace with Atom
FACT = Tuple[Predicate, List[Any]]

@lru_cache
def predicate_file(directory: str, predicate: Predicate) -> TextIO:
    path = Path(directory)
    path.mkdir(exist_ok=True, parents=True)
    return open(path / f'{predicate}.facts', 'w', encoding='utf-8')


def emit_fact(directory: str, fact: FACT):
    file = predicate_file(directory, fact[0])


def tuple_as_str(fact: FACT) -> str:
    """
    Convert a predicate and arguments to a TSV tuple

    >>> print(tuple_as_str((Predicate.SV, ['/persons', '/a'])))
    sv(/persons, /a)

    :param predicate:
    :param args:
    :return:
    """
    predicate = fact[0]
    args = fact[1]
    return f"{predicate.value}(" + ', '.join([str(a) for a in args]) + ")"

def pp_facts(facts: Iterable[FACT], hide: Optional[List[Predicate]]=None) -> None:
    """
    Pretty print a set of TSV tuples.

    >>> pp_facts([(Predicate.SV, ['/persons', '/a'])])
    sv(/persons, /a)

    :param facts:
    :param hide:
    :return:
    """
    for fact in facts:
        if hide and fact[0] in hide:
            continue
        print(tuple_as_str(fact))


def object_to_tuples(obj: Any, directory: str=None, path=None) -> Iterator[FACT]:
    """
    Convert a dictionary to a set of TSV tuples

    >>> pp_facts(object_to_tuples({'a': 1}), hide=[Predicate.PATH])
    sv(., a, ./a)
    literal_number(./a, 1)

    >>> pp_facts(object_to_tuples({'a': True}), hide=[Predicate.PATH])
    sv(., a, ./a)
    literal_boolean(./a, True)


    >>> pp_facts(object_to_tuples({'a': "x"}), hide=[Predicate.PATH])
    sv(., a, ./a)
    literal_string(./a, x)

    >>> pp_facts(object_to_tuples({'l': [1]}), hide=[Predicate.PATH])
    sv(., l, ./l)
    nth(./l, 0, ./l/[0])
    literal_number(./l/[0], 1)

    >>> pp_facts(object_to_tuples({'persons': {"P1": {"name": "n1"}}}), hide=[Predicate.PATH])
    sv(., persons, ./persons)
    sv(./persons, P1, ./persons/P1)
    sv(./persons/P1, name, ./persons/P1/name)
    literal_string(./persons/P1/name, n1)

    :param obj:
    :param directory:
    :param path:
    :return:
    """
    if path is None:
        path = '.'
    yield Predicate.PATH, [path, path]
    if isinstance(obj, dict):
        for k, v in obj.items():
            k = str(k).replace("/", "__SLASH__")
            child_path = f"{path}/{k}"
            yield Predicate.SV, [path, k, child_path]
            yield from object_to_tuples(v, directory, child_path)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            child_path = f"{path}/[{i}]"
            yield Predicate.NTH, [path, i, child_path]
            yield from object_to_tuples(v, directory, child_path)
    else:
        if obj is None:
            yield Predicate.LITERAL_NULL, [path]
        elif isinstance(obj, str):
            yield Predicate.LITERAL_STRING, [path, obj]
        elif isinstance(obj, bool):
            yield Predicate.LITERAL_BOOLEAN, [path, obj]
        elif isinstance(obj, Number):
            yield Predicate.LITERAL_NUMBER, [path, obj]
        else:
            raise ValueError(f'Cannot handle {type(obj)}')



class JsonFactsDumper(Dumper):
    """
    Dumps JSON objects as TSV tuples
    """

    def dump(self, element: Union[YAMLRoot, Dict, BaseModel], directory=None, **kwargs):
        """
        Dump a LinkML instance as TSV tuples, saving to a directory

        :param element:
        :param schemaview:
        :param directory:
        :param kwargs:
        :return:
        """
        if isinstance(element, BaseModel):
            element = element.dict()
        elif isinstance(element, YAMLRoot):
            element = yaml_dumper.dumps(element)
        elif not isinstance(element, dict):
            raise ValueError(f'Cannot dump {type(element)}')
        object_to_tuples(g, directory=directory)

    def dumps(self, *args, **kwargs) -> str:
        """
        Dump a LinkML instance as TSV tuples, returning a string
        :param args:
        :param kwargs:
        :return:
        """
        # return self.dump(*args, **kwargs)
        raise NotImplementedError

    def dict_to_tuples(self, graph: Graph, directory: str) -> None:
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




