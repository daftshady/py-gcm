py-gcm
======

Python wrapper for google cloud messaging.

It can help to send push message for android device using google cloud messaging.

Supports some retry handling when gcm server is gone and provides automatic
chunking when number of sender is larger than gcm limitation at one go.
You can add some gcm options like `collapse_key` easily.

py-gcm 0.3 runs on
- Python (2.6, 2.7, 3.2, 3.3)
 
Installation
------------

      $ pip install pygcm
      
      
Usage
-----

      >>> from pygcm.manage import GCMManager
      >>> m = GCMManager('sender_id_from_google')
      >>> ids = ['gcm', 'device', 'keys']
      >>> m.send(ids, 'message')
      [{u'failure': 0, u'canonical_ids': 0, u'success': 3, ...}]
      ...




