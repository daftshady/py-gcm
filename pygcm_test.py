# -*- coding:utf-8 -*-
"""

Pygcm unittests

"""

import unittest
from pygcm.manage import GCMManager
from pygcm.base_config import MAX_NUMBER_OF_TARGET


class ManagerTest(unittest.TestCase):
    def setUp(self):
        self.m = GCMManager('AIzaSyD4oHRDjZozFMTiIUVF8JlpNfOVEhLLwMQ')
        self.id = """
                APA91bH78Ahg7bLK_9JzN0jEo-Z5qWB-8jP-NA9eZFzMEZ0G
                gIReXuSpeyIL23Hei8VfAQmaM_qEWLIznK2EYLLgl8s7oRQX
                Hxgc3W77IqBR7WjQyiHU-fcKjDp_FF4v1MvP3SuDTVyjJXlp
                NXmbrxPN-48WSQlJIg
                """
        self.message = 'pygcm test'
    
    def test_single_send(self):
        success = self.m.send(self.id, self.message)
        self.assertTrue(success)

    def test_multi_send(self):
        ids = [self.id] * MAX_NUMBER_OF_TARGET
        success = self.m.send(ids, self.message)
        self.assertTrue(success)

    def test_multi_send_split(self):
        ids = [self.id] * MAX_NUMBER_OF_TARGET * 3
        success = self.m.send(ids, self.message)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
