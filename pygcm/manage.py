# -*- coding:utf-8 -*-
"""

    pygcm.manage
    ~~~~~~~~~~~~

    Provides external apis.

"""

import json
from collections import Iterable
from pygcm.compat import urllib2, basestring
from pygcm.exceptions import GCMException, ParamTypeError
from pygcm.base_config import MAX_NUMBER_OF_TARGET
from pygcm.request import RequestHandler, RequestBuilder


def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]


class GCMManager(object):
    """GCMManager
    Provides the way to actually send request.
    User should use this class to access gcm.

    Basic Usage::

        >>> from pygcm.manage import GCMManager
        >>> m = GCMManager('__gcm api key provided by google__')
        >>> ids = ['android', 'device', 'keys']
        >>> m.send(ids, 'hello python!')
        >>> id = 'android_device_key'
        >>> m.send(id, 'hello python!')

    """

    retry = 3

    def __init__(self, api_key=None,
                split_num=MAX_NUMBER_OF_TARGET, retry=None):
        """Initialize GCMManager
        split_num must not exceed MAX_NUMBER_OF_TARGET
        Max number of device key that can be on request
        at one go is fixed by google api."""
        if not isinstance(api_key, basestring):
            raise GCMException("Invalid api key")

        if not isinstance(split_num, int) or \
                split_num > MAX_NUMBER_OF_TARGET:
            raise GCMException("Invalid split_num")

        self.split_num = split_num
        self.retry = retry if isinstance(retry, int) else self.retry
        self.api_key = api_key

    def single_send(self, id_=None, collapse_key=None,
            time_to_live=None, delay_while_idle=None,
            data=None, message=None):
        if not isinstance(id_, basestring):
            raise ParamTypeError("Wrong id type")

        return self.multi_send(ids=[id_], collapse_key=collapse_key,
                        time_to_live=time_to_live,
                        delay_while_idle=delay_while_idle,
                        data=data, message=message)

    def multi_send(self, ids=None, collapse_key=None,
            time_to_live=None, delay_while_idle=None,
            data=None, message=None):
        if not isinstance(ids, Iterable):
            raise ParamTypeError("Wrong ids type")

        split = len(ids) > self.split_num
        b = RequestBuilder(self.api_key)

        b.add_options(collapse_key=collapse_key,
                            time_to_live=time_to_live,
                            delay_while_idle=delay_while_idle)
        b.add_whole_data(data)
        if message is not None:
            b.add_message(message)

        resps = []
        def _wrap_send(req):
            resp = self._send(req)
            resp = self._handle_retry(req) if resp is None else resp
            return resp

        if split:
            chunked_ids = chunks(ids, self.split_num)
            for chunk in chunked_ids:
                resps.append(
                    _wrap_send(b.add_devices_and_rebuild(chunk))
                )
        else:
            b.add_devices(ids)
            resps.append(_wrap_send(b.build()))
        return resps

    def _handle_retry(self, request):
        for _ in range(self.retry):
            resp = self._send(request)
            if resp is not None:
                break

        if resp is not None:
            return resp
        raise GCMException('Failed to send a message')

    def _send(self, request):
        return request.post()

    def send(self, id_, message, data=None, assert_success=False):
        """This method uses default setting(with no additional args)
        to send a message
        Returns `list` of response `dict`.

        TODO: Customized exception handling is difficult.
        Should return more information instead of only returning
        success status. """
        success = False

        if isinstance(id_, basestring):
            success = self.single_send(id_=id_, message=message,
                            data=data)
        elif isinstance(id_, Iterable):
            success = self.multi_send(ids=id_, message=message,
                            data=data)
        else:
            raise ParamTypeError("Wrong id type")

        return success
