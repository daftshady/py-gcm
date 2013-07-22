# -*- coding:utf-8 -*-
"""

    pygcm.request.base

    Request related modules.

"""

import json
import urllib2
from pygcm.request.config import r_type
from collections import Iterable
from pygcm.configs.base_config import SENDER_URL, HEADERS, PARAMS, \
                                MAX_NUMBER_OF_TARGET, CONTENT_TYPE

class RequestHandler(object):
    """Requests wrapper 
    Handles requests holding specific configuation"""

    def __init__(self, **kwargs):
        super(RequestHandler, self).__init__()
        self._url = kwargs.get('url', None)
        self._headers = kwargs.get('headers', None) or {}
        self._params = kwargs.get('params', None) or {}
        self.proxies = kwargs.get('proxies', None)
        
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
        """Can add another 'ready' status like host is alive or not, is header proper.. etc """
        return self._url is not None and \
                self._params is not None and \
                self._headers is not None

    def _send(self, request_type, 
                headers=None, params=None):
        """Each send funtion sends a request. Returns :class:responseobject.
        :param headers: should contains authorization header including api-key.
        :param params: should contains device key.(Others are options)
        """
        if request_type != r_type.post:
            raise GCMException("Google does not support other methods yet")

        if not self.ready:
            raise GCMException("RequestHandler not ready")

        request = urllib2.Request(self._url,
                        data=params or self._params,
                        headers=headers or self._headers)
        return urllib2.urlopen(request)

    def get(self, headers=None, params=None):
        return self._send(r_type.get, headers=headers, params=params)

    def post(self, headers=None, params=None):
        return self._send(r_type.post, headers=headers, params=params)

    def put(self, headers=None, params=None):
        return self._send(r_type.put, headers=headers, params=params)

    def patch(self, headers=None, params=None):
        return self._send(r_type.patch, headers=headers, params=params)

    def delete(self):
        return self._send(r._type.delete)


class RequestBuilder(object):
    """RequestBuilder for GCM.
    Can add various data into request params."""

    def __init__(self, api_key, content_type=None):
        """Initialize request builder.
        Auth key should be prefixed by 'key='.
        Default content type is 'json', 
        """
        content_type = content_type or CONTENT_TYPE.JSON

        if not isinstance(api_key, basestring):
            raise GCMException("Invalid api key")
        
        auth_key = 'key=' + api_key
        self._url = SENDER_URL
        self._headers = dict.fromkeys(HEADERS, None)
        self._params = dict.fromkeys(PARAMS, None)
        self._data = dict()
        self._construct_headers(auth_key, content_type)

    def _construct_headers(self, authorization, content_type):
        self._headers.update({'Content-Type' : content_type,
                            'Authorization' : authorization})
    
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
        self._params.update({'collapse_key' : collapse_key,
                            'delay_while_idle' : delay_while_idle,
                            'time_to_live' : time_to_live})
    
    def add_data(self, k, v):
        self._data.update({k:v})
    
    def add_message(self, msg):
        self.add_data('message', msg)

    def add_headers(self, k, v):
        self._headers.update({k:v})
    
    def _remove_option(self, k):
        if self._params.get(k, None) is None:
            self._params.pop(k, None)
    
    def _clean_params(self):
        map(lambda k : self._remove_option(k), PARAMS)

    def _get_content_type(self):
        return self._headers.get('Content-Type', '')

    def build(self):
        self._clean_params()
        self._params.update({'data' : self._data})
        params = json.dumps(self._params) \
            if self._is_json_request() else self._params
        return RequestHandler(url=self._url,
                                headers=self._headers,
                                params=params)
    
    def _is_json_request(self):
        return 'json' in self._get_content_type()

    def flush(self):
        self._params = dict.fromkeys(PARAMS, None)
        self._data = dict()

