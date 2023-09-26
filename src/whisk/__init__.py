"""Proportioned combination of RDataFrame data structures"""

from ._whisk import whisk
from ._table import table
from ._version import version as __version__  # noqa

__all__ = ["whisk", "table"]