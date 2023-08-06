"""
********************************************************************************
to_delete
********************************************************************************

.. currentmodule:: to_delete


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os


__author__ = ["Li"]
__copyright__ = ""
__license__ = "MIT License"
__email__ = ""
__version__ = "0.3.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]
