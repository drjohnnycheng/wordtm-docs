# __init__.py
#
# Root package
#
# Copyright (c) 2022-2024 WordTM Project 
# Author: Johnny Cheng <drjohnnycheng@gmail.com>
#
# Updated: 2 February 2024
#
# URL: https://github.com/drjohnnycheng/wordtm.git
# For license information, see LICENSE.TXT

#: Package version information
from .version import __author__
from .version import __copyright__
from .version import __credits__
from .version import __license__
from .version import __version__
from .version import __email__
from .version import __status__
from .version import __url__

from .meta import addin_all

#: Add the additional features (timing and showing code) to all functions
#:   of the module "wordtm"
addin_all()
