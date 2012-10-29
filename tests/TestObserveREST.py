# coding=utf-8

from datetime import datetime
from threading import Timer
import unittest
from pycolo.codes import codes, mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.resource import Resource

class Observe(Resource):
    """
    Observable resource which changes every 5 seconds.

    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.
    TD_COAP_OBS_01
    TD_COAP_OBS_02
    TD_COAP_OBS_03
    TD_COAP_OBS_04
    TD_COAP_OBS_05
    """
    #  The current time represented as string
    time = ""

    def __init__(self):
        self.title = "Observable resource which changes every 5 seconds"
        self.resourceType = "observe"
        self.observable = True
        Timer(5.0, self._update).start()  # Set timer task scheduling

    def _update(self):
        """ Defines a new timer task to return the current time """
        self.time = datetime.datetime.now().strftime("%H:%m:%S")
        self.changed()  # Call changed to notify subscribers

    def performGET(self, request):
        response = Response(codes.RESP_CONTENT)
        response.payload = self.time
        response.contentType = mediaCodes.text
        response.maxAge = 5
        request.respond(response)  # complete the request

class RESTObserver(Resource):
    """
    Provide an HTTP REST interface to monitor and control observation mechanisms.
    """
    pass


class TestObserveREST(unittest.TestCase):

    def setUp(self):
        server = Endpoint()
        res = Observe()
        server.addResource(res)

    def test_monitor(self):
        raise NotImplementedError

if __name__ == '__main__':
    unittest.main()
