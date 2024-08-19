"""Define object types for the bookbot project."""

import typing

import collections
import pathlib
import os


PathLike = typing.Union[str, pathlib.Path, os.PathLike, None]
DictLike = typing.Union[dict, collections.defaultdict]
