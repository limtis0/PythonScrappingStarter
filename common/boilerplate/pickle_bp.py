import os
import pickle
from typing import Any, Union


def dump(data: Any, path: Union[str, bytes, os.PathLike]) -> None:
    with open(path, 'wb') as file:
        pickle.dump(data, file)


def load(path: Union[str, bytes, os.PathLike], default=None):
    if not os.path.exists(path):
        if default is not None:
            return default
        raise OSError(f'Directory {path} can not be found.')

    with open(path, 'rb') as file:
        return pickle.load(file)
