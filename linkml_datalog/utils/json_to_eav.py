from dataclasses import dataclass
from datetime import date, datetime

import click
import json
import yaml
import hashlib
from io import StringIO
from contextlib import redirect_stdout
from enum import Enum
from typing import Dict, List, Any, Union, Tuple

DICT_OR_LIST = Union[Dict, List]

class ObjType(Enum):
    LIST = 'l'
    DICT = 'd'
    NUMBER = 'n'
    STRING = 's'
    BOOLEAN = 'b'
    NONE = 'x'
    DOCUMENT = 'r'


HDR = ['id', 'index', 'key', 'val_s', 'val_i', 'type']

@dataclass
class EavDumper:
    """
    Exports arbitrary JSON or Dict objects to EAV-style TSV
    """
    dict_list: List[Dict] = None

    def dumps(self, obj: DICT_OR_LIST, header=False, document_root: Union[dict, str] = None) -> str:
        """
        Dumps a dict to an EAV TSV string

        :param obj:
        :param header:
        :param document_root:
        :return:
        """
        output = StringIO()
        if document_root is not None:
            if isinstance(document_root, str):
                document_root = {
                    '_id': document_root
                }
            document_root['_contents'] = obj
            obj = document_root
        with redirect_stdout(output):
            if header:
                self._header()
            self._dumps(obj)
        return output.getvalue()

    def dump(self, obj: DICT_OR_LIST, file, header=False, **kwargs) -> None:
        """
        Dumps a dict to an EAV TSV file

        :param obj:
        :param header:
        :return:
        """
        with redirect_stdout(file):
            if header:
                self._header()
            self._dumps(obj, **kwargs)

    def as_objs(self, obj: DICT_OR_LIST) -> List[Dict]:
        self.dict_list =[]
        self._dumps(obj)
        r = self.dict_list
        self.dict_list = None
        return r

    def _header(self):
        print("\t".join(HDR))

    def _dumps(self, obj: Any) -> Tuple[Any, ObjType]:
        if isinstance(obj, list):
            id = self._id(obj)
            ix = 0
            for v in obj:
                v2, t = self._dumps(v)
                self.tuple(id, index=ix, key=str(ix), val=v2, type=t)
                ix += 1
            return id, ObjType.LIST
        elif isinstance(obj, dict):
            id = self._id(obj)
            ix = 0
            for k, v in obj.items():
                v2, t = self._dumps(v)
                self.tuple(id, index=ix, key=k, val=v2, type=t)
                ix += 1
            return id, ObjType.DICT
        elif obj is None:
            return obj, ObjType.NONE
        elif isinstance(obj, bool):
            return obj, ObjType.BOOLEAN
        elif isinstance(obj, date) or isinstance(obj, datetime):
            return str(obj), ObjType.STRING
        elif isinstance(obj, float) or isinstance(obj, int):
            return obj, ObjType.NUMBER
        else:
            return str(obj), ObjType.STRING

    def _id(self, obj: DICT_OR_LIST) -> str:
        s = json.dumps(obj, sort_keys=True)
        h = hashlib.md5(str(s).encode('utf-8')).hexdigest()
        # https://datatracker.ietf.org/doc/html/draft-thiemann-hash-urn-01
        return f'urn:hash::md5:{h}'

    def tuple(self, id: str, key: str, index: int, val: Any, type: ObjType):
        if isinstance(val, str):
            val_s = val
            val_i = 0
        elif isinstance(val, bool):
            val_i = int(val)
            val_s = str(val)
        else:
            val_i = val
            val_s = str(val)
        t = [id, index, key, val_s, val_i, type.value]
        t = [str(x).replace("\t","\\t").replace("\n", "\\n") for x in t]
        if self.dict_list is not None:
            self.dict_list.append(dict(id=id, key=key, index=index, val_s=val_s, val_i=val_i, type=type.value))
        else:
            print("\t".join(t))

def add_document_root(obj: Any, path: str) -> Dict:
    document_root = {'_id': path,
                     '_type': 'document',
                     '_contents': obj}
    return document_root


@click.command()
@click.option('--output', '-o', help='Path to output file')
@click.option('--header/--no-header', default=False, help='include a TSV header')
@click.option('--add-root/--no-add-root', default=False, help='include a document root')
@click.option('--type', '-t', help='inject top level type')
@click.argument('input')
def main(input, output, type, add_root: bool, **args):
    with open(input, 'rb') as stream:
        obj = yaml.safe_load(stream)
    if type is not None:
        obj['@type'] = type
    if add_root:
        obj = add_document_root(obj, input)
    dumper = EavDumper()
    if output is None:
        print(dumper.dumps(obj, **args))
    else:
        with open(output, 'w') as stream:
            dumper.dump(obj, stream, **args)

if __name__ == "__main__":
    main()
