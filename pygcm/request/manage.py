# -*- coding:utf-8 -*-
"""

    pygcm.request.manage
    ~~~~~~~~~~~~~~~~~~~~

    Provides actual user shortcuts.

"""

import json
import urllib2
from types import IntType
from pygcm.exception.exceptions import GCMException, ParamTypeError, FatalError
from pygcm.configs.base_config import PARAMS, SENDER_URL, HEADERS, MAX_NUMBER_OF_TARGET
from pygcm.request.base import RequestHandler, RequestBuilder
from collections import Iterable
from pygcm.common.utils import chunks
from pygcm.request.config import status_group


class GCMManager(object):
    """GCMManager
    Provides the way to actually send request.
    Provides shortcuts for gcm.
    User should use this class to access gcm."""
    
    retry = 3

    def __init__(self, api_key=None, 
                split_num=MAX_NUMBER_OF_TARGET, retry=None):
        """Initialize GCMManager
        split_num must not exceed MAX_NUMBER_OF_TARGET
        Max number of device key that can be on request at one go is fixed by google api."""
        if not isinstance(api_key, basestring):
            raise GCMException("Invalid api key")

        self.split_num = split_num if isinstance(split_num, IntType) \
                            else MAX_NUMBER_OF_TARGET
        self.retry = retry if isinstance(retry, IntType) \
                            else self.retry

        self.api_key = api_key
        builder = RequestBuilder(self.api_key)


    def single_send(self, id=None, collapse_key=None,
            time_to_live=None, delay_while_idle=None,
            data=None, message=None):
        if not isinstance(id, basestring):
            raise ParamTypeError("Wrong id type")

        self.multi_send(ids=[id], collapse_key=collapse_key,
                        time_to_live=time_to_live, delay_while_idle=delay_while_idle,
                        data=data, message=message)


    def multi_send(self, ids=None, collapse_key=None,
            time_to_live=None, delay_while_idle=None,
            data=None, message=None):
        if not isinstance(ids, Iterable):
            raise ParamTypeError("Wrong ids type")
        
        split = True if len(ids) > self.split_num else False
        b = RequestBuilder(self.api_key)

        b.add_options(collapse_key=collapse_key,
                            time_to_live=time_to_live,
                            delay_while_idle=delay_while_idle)
        b.add_whole_data(data)
        if message is not None:
            b.add_message(message)
        
        success = False
        if split:
            chunked_ids = chunks(ids, self.split_num)
            for chunk in chunked_ids:
                request = b.add_devices_and_rebuild(chunk)
                success = self._send(request)
                if not success and \
                    not self._handle_retry(request):
                    break

        else:
            b.add_devices(ids)
            request = b.build()
            success = self._send(request)
            if not success:
                self._handle_retry(request)

    def _handle_retry(self, request):
        for _ in range(self.retry):
            if self._send(request):
                return True
        return False

    def _send(self, request):
        try:
            request.post()
        except urllib2.HTTPError, e:
            if e.code in status_group.fail:
                raise FatalError("Request failed with unexpected error")

            if e.code in status_group.retryable:
                return False
        return True

    def send_message(self, id, message, data=None):
        """This method uses default setting(with no additional args) 
        to send a message"""
        if isinstance(id, basestring):
            self.single_send(id=id, message=message,
                            data=data)
        elif isinstance(id, Iterable):
            self.multi_send(ids=id, message=message,
                            data=data)
        else:
            raise ParamTypeError("Wrong id type")

