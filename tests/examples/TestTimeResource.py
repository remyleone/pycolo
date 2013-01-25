# coding=utf-8

"""
Testing a typical observed resource.
"""

import unittest

from datetime import datetime
from pycolo.endpoint import Endpoint

import pycolo as coap
from pycolo.codes import codes
from pycolo.resource import Resource


class TestTimeResource(unittest.TestCase):
    """
    Observing time resource
    """

    def setUp(self):
        """
        Setup a CoAP server and assign a TimeResource to it
        """
        self.server = Endpoint(__name__)

        class TimeResource(Resource):
            """
            Simple Time Resource that give the time and support observation.

            :return:
            """

            def __call__(self):
                """
                Resource that returns the current time on a GET request.
                It also Supports observing.
                """
                self.time = datetime.datetime.now()
                self.changed()  # Call changed to notify subscribers
                return self.time

        self.server.add_url_rule("/time", obs=True,
                      methods=["GET", "POST"],
                      resource=TimeResource(title="CurrentTime"))

    def test_get(self):
        """
        Simple get test
        """
        r = coap.get(self.server.url + "/time")
        self.assertEqual(r.status, codes.ok)

    def test_observe(self):
        """
        Implement a simple observe process
        """
        r = coap.observe(self.server.url + "/time")
        self.assertEqual(codes.ok, r.code)

if __name__ == '__main__':
    unittest.main()
