# -*- coding:utf-8 -*-
"""

    pygcm.exceptions
    ~~~~~~~~~~~~~~~~
    
    Define gcm related exceptions.

"""

class GCMException(Exception):
    """Basic GCM exception"""
    pass


class TemporalServerError(GCMException):
    """GCM server is temporally unavailable"""
    pass


class ParamTypeError(GCMException):
    """When GCM params has invalid form"""
    pass
