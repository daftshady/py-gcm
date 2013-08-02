# -*- coding:utf-8 -*-
"""

    pygcm.exception.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Define gcm related exceptions.

"""

class GCMException(Exception):
    """Basic GCM exception"""
    pass

class InternalError(GCMException):
    """GCM server has internal problem"""
    pass

class TemporalServerError(GCMException):
    """GCM server is temporally unavailable"""
    pass

class ParamTypeError(GCMException):
    """When GCM params has strange type"""
    pass

class FatalError(GCMException):
    """When request to GCM has failed and our client has problem."""
    pass
