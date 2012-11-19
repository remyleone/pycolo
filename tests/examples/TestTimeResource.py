# coding=utf-8

"""
TODO
"""

import unittest

from datetime import datetime
from threading import Timer
from pycolo.endpoint import Endpoint

from pycolo.request import request
from pycolo.resource import Resource
from pycolo.codes import mediaCodes, codes


class TimeResource(Resource):
    """
    Defines a resource that returns the current time on a GET request.
    It also Supports observing.
    """

    def __init__(self):

        def update(self):
            """ generated source for method run """
            self.time = datetime.datetime.now()
            #  Call changed to notify subscribers
            self.changed()

        self.title = "GET the current time"
        self.resourceType = "CurrentTime"
        self.isObservable = True
        #  Set timer task scheduling
        timer = Timer(2, update)
        timer.start()

    def performGET(self, request):
        """

                :param request:
                """
        request.respond(codes.RESP_CONTENT, self.time, mediaCodes.txt)


class TestSeparate(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        Setup a CoAP server and assign a TimeResource to it
        """
        res = TimeResource()
        server = Endpoint()
        server.addResource(res)

    def test_get(self):
        """
        Simple get test
        """
        r = request.get("coap://localhost:5683/time")
        self.assertEqual(r.status, codes.ok)

if __name__ == '__main__':
    unittest.main()
