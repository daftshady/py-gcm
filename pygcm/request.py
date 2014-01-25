# -*- coding:utf-8 -*-
"""

    pygcm.request
    ~~~~~~~~~~~~~

    Request related modules.

"""

import json
from collections import Iterable
from pygcm.exceptions import GCMException
from pygcm.compat import urllib2, urlencode, basestring
from pygcm.base_config import SENDER_URL, DEFAULT_ENCODING


# HTTP request constants declaration
def enum(**enums):
    return type('Enum', (), enums)

method = enum(
    get = 'GET',
    post = 'POST',
    put = 'PUT',
    delete = 'DELETE',
    patch = 'PATCH'
    )

status_code = enum(
    success = 200,
    invalid_field = 400,
    auth_failed = 401,
    internal_error = 500,
    service_unavailable = 503
    )

status_group = enum(
    fail = [status_code.auth_failed,
            status_code.invalid_field],
    success = [status_code.success],
    retryable = [status_code.internal_error,
                status_code.service_unavailable]
    )


class RequestHandler(object):
    """Requests wrapper 
    Handles requests holding specific configuation"""

    def __init__(self, **kwargs):
        self._url = kwargs.get('url')
        self._headers = kwargs.get('headers', {})
        self._params = kwargs.get('params', {})
        self.proxies = kwargs.get('proxies', {})
        
        if self.proxies:
            if isinstance(self.proxies, dict):
                urllib2.install_opener(
                    urllib2.build_opener(
                        urllib2.ProxyHandler(self.proxies)))
            
    @property
    def url(self):
        return self._url

    @property
    def headers(self):
        return self._headers

    @property
    def params(self):
        return self._params

    @property
    def ready(self):
        """Can add another 'ready' status """
        return self._url is not None

    def _send(self, request_type, headers=None, params=None):
        """Each send funtion sends a request.

        :param headers: should contains authorization header including api-key.
        :param params: should contains device key. (Others are options)
        """
        if request_type != method.post:
            raise GCMException("Google does not support other methods yet")

        if not self.ready:
            raise GCMException("RequestHandler is not ready to send")
        
        p = params or self._params
        request = urllib2.Request(self._url,
                        data=p.encode(DEFAULT_ENCODING),
                        headers=headers or self._headers)

        try:
            urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            if e.code in status_group.fail:
                raise GCMException(
                    "Request failed with unexpected error : code " + e.code)
            if e.code in status_group.retryable:
                return False
            raise GCMException(e)

        return True

    def post(self, headers=None, params=None):
        return self._send(method.post, headers=headers, params=params)


class RequestBuilder(object):
    """RequestBuilder for GCM.
    Can add various data into request params."""

    _HEADERS = ['Content-Type', 'Authorization']
    _PARAMS = [
        'registration_ids', 'collapse_key',
        'data', 'delay_while_idle', 'time_to_live'
        ]
    _CONTENT_TYPE_JSON = 'application/json'

    def __init__(self, api_key, content_type=None):
        """Initialize request builder.
        Auth key should be prefixed by 'key='.
        Default content type is 'json', 
        """
        content_type = content_type or self._CONTENT_TYPE_JSON

        if not isinstance(api_key, basestring):
            raise GCMException("Invalid api key")
        
        auth_key = 'key=' + api_key
        self._url = SENDER_URL
        self._headers = dict.fromkeys(self._HEADERS, None)
        self._params = dict.fromkeys(self._PARAMS, None)
        self._data = dict()
        self._construct_headers(auth_key, content_type)

    def _construct_headers(self, authorization, content_type):
        self._headers.update({
                'Content-Type' : content_type,
                'Authorization' : authorization
                })
    
    def add_devices(self, ids):
        if not isinstance(ids, Iterable):
            raise GCMException("Should add list object in id params.")
        self._params.update({'registration_ids' : ids})
    
    def add_whole_data(self, data):
        self._params.update({'data' : data})

    def add_devices_and_rebuild(self, ids):
        self.add_devices(ids)
        return self.build()

    def add_options(self, collapse_key=None, 
                    delay_while_idle=None, time_to_live=None):
        self._params.update({
                'collapse_key' : collapse_key, 
                'delay_while_idle' : delay_while_idle,
                'time_to_live' : time_to_live
                })
    
    def add_data(self, k, v):
        self._data.update({k : v})
    
    def add_message(self, msg):
        self.add_data('message', msg)

    def add_headers(self, k, v):
        self._headers.update({k : v})
    
    def _remove_option(self, k):
        if self._params.get(k) is None:
            self._params.pop(k, None)
    
    def _clean_params(self):
        map(lambda k : self._remove_option(k), self._PARAMS)

    def _get_content_type(self):
        return self._headers.get('Content-Type', '')

    def build(self):
        self._clean_params()
        self._params.update({'data' : self._data})

        params = json.dumps(self._params) \
            if self._json_request() else urlencode(self._params)
        return RequestHandler(url=self._url,
                                headers=self._headers,
                                params=params)
    
    def _json_request(self):
        """Returns True if request content type of request is json"""
        return 'json' in self._get_content_type()

    def flush(self):
        self._params = dict.fromkeys(self._PARAMS, None)
        self._data = dict()

