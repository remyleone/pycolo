# coding=utf-8

"""
TODO
"""

import unittest

from datetime import datetime
from pycolo.endpoint import Endpoint

from pycolo.request import request
from pycolo.codes import codes


class TestSeparate(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        Setup a CoAP server and assign a TimeResource to it
        """
        server = Endpoint(__name__)

        @server.route("/time", obs=True, repeat=2,
                      title="CurrentTime",
                      methods=["GET", "POST"])
        def update(self):
            """
            Defines a resource that returns the current time on a GET request.
            It also Supports observing.
            """
            self.time = datetime.datetime.now()
            #  Call changed to notify subscribers
            self.changed()
            return self.time

    def test_get(self):
        """
        Simple get test
        """
        r = request.get("coap://localhost:5683/time")
        self.assertEqual(r.status, codes.ok)

    def test_observe(self):
        """
        Implement a simple observe process
        """
        pass

if __name__ == '__main__':
    unittest.main()
