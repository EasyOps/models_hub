import yaml
import json
import toml

import os
import pathlib
from typing import Dict, Union
from error_handling import FileNotSupported


class Loader(yaml.SafeLoader):

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__()

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            with open(filename, "r") as f:
                return yaml.load(f, Loader)
        else:
            raise "File must be end with yaml or yml"


Loader.add_constructor("!include", Loader.inclue)

def load_from_yaml(fname: str) -> Dict:
    with open(fname, "r", encoding="utf-8") as f:
        base_config = yaml.load(f, Loader=Loader)
    return base_config


def load_from_json(fname: str) -> Dict:
    with open(fname, "r", encoding="utf-8") as f:
        base_config = json.load(f)
    return base_config

def load_from_toml(fname: str) -> Dict:
    base_config = toml.load(fname)
    return base_config


class Cfg(dict):

    def __init__(self, config_dict: Dict) -> None:
        super(Cfg, self).__init__(**config_dict)
        self.__dict__ = self
    
    @staticmethod
    def load_config_from_file(fname: str) -> Dict:
        if not os.path.exists(fname):
            raise FileNotFoundError(f"Not found config at {fname}")
        if fname.endswith(".json"):
            return Cfg(load_from_json(fname))
        elif fname.endswith(".yaml") or fname.endswith(".yml"):
            return Cfg(load_from_yaml(fname))
        elif fname.endswith(".toml"):
            return Cfg(load_from_toml(fname))
        else:
            raise FileNotSupported(fname=fname)

    def save(self, fname : str) -> None:
        with open(fname, "w", encoding="utf-8") as outfile:
            if fname.endswith(".json"):
                json.dump(dict(self), outfile, ensure_ascii=False)
            elif fname.endswith(".yaml") or fname.endswith(".yml"):
                yaml.dump(dict(self), outfile, default_flow_style=False, allow_unicode=True)
            elif fname.endswith(".toml"):
                toml.dump(dict(self), outfile)
            else:
                raise FileNotFoundError(fname=fname)

