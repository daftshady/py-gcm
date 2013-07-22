from pygcm.common.utils import enum

SENDER_URL = 'https://android.googleapis.com/gcm/send'

PARAMS = ['registration_ids',
          'collapse_key',
          'data',
          'delay_while_idle',
          'time_to_live']

HEADERS = ['Content-Type',
           'Authorization']

MAX_NUMBER_OF_TARGET = 1000

CONTENT_TYPE = enum(PLAIN='test/plain', 
                    JSON='application/json')

