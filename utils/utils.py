from collections.abc import Callable
from typing import Dict, ParamSpec, TypeVar
import importlib



P = ParamSpec('P')
R = TypeVar('R')


def load_module(path: str, args: Dict = None, initialize: bool = True) -> Callable[P, R]:
    module_path = ".".join(path.split(".")[:-1])
    class_of_function_name = path.split(".")[-1]
    module = importlib.import_module(module_path)
    class_of_function = getattr(module, class_of_function_name)

    if initialize:
        if args:
            return class_of_function(**args)
        else:
            return class_of_function()
    else:
        return class_of_function
     

