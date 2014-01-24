# -*- coding:utf-8 -*-
"""

    pygcm.compat
    ~~~~~~~~~~~~

    Python 2.x and 3.x compatibility

"""

import sys

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

ver = sys.version_info

is_py2 = (ver[0] == 2)
is_py3 = (ver[0] == 3)

if is_py2:
    from urllib import urlencode
    basestring = basestring

elif is_py3:
    from urllib.parse import urlencode
    basestring = (str, bytes)

