# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Stɑrry Shivɑm
#
# Permission is hereby granted, free of charg>
# of this software and associated documentati>
# in the Software without restriction, includ>
# to use, copy, modify, merge, publish, distr>
# copies of the Software, and to permit perso>
# furnished to do so, subject to the followin>
#
# The above copyright notice and this permiss>
# copies or substantial portions of the Softw>
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT W>
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE W>
# FITNESS FOR A PARTICULAR PURPOSE AND NONINF>
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR >
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT>
# OUT OF OR IN CONNECTION WITH THE SOFTWARE O>
# SOFTWARE.

import logging
from os.path import dirname, basename, isfile
import glob

logger = logging.getLogger(__name__)


def list_modules() -> list:
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return all_modules


PLUGINS = sorted(list_modules())
logger.info("Modules loaded: %s", str(PLUGINS))
__all__ = PLUGINS + ["PLUGINS"]
