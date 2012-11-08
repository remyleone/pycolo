# coding=utf-8
import unittest

from pycolo.codes import codes
from pycolo.codes import mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.request import request
from pycolo.resource import Resource


class LongPathResource(Resource):
    """
    Long path ressource

    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.

    TD_COAP_CORE_12
    """

    def __init__(self):
        self.title = "Long path resource"
        self.name = "/seg1/seg2/seg3 "

    def performGET(self, request):
        response = Response(codes.RESP_CONTENT)
        response.payload = str(request)
        response.contentType = mediaCodes.text
        request.respond(response)


class LongPathTest(unittest.TestCase):
    def setUp(self):
        """
        Initial set up of the resource.
        """
        server = Endpoint()
        res = LongPathResource()
        server.register(res)
        pass

    def test_GET_LongPath(self):
        """
        Identifier: TD_COAP_CORE_12
        Objective: Handle request containing several URI-Path options
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a /seg1/seg2/seg3 resource

        Step 1 (stimulus) Client is requested to send a confirmable GET request to server’s resource

        Step 2 (Check (CON)) Sent request must contain:
            • Type = 0 (CON)
            • Code = 1 (GET)
            • Option type = URI-Path (one for each path segment)

        Step 3 (Check (CON)) Server sends response containing:
            • Code = 69 (2.05 content)
            • Payload = Content of the requested resource
            • Content type option

        Step 4 (Verify (IOP)) Client displays the response

        Simple get on the long path resource.
        Step 1 (stimulus): Client is requested to send a confirmable GET request to
        server’s resource

        """
        r = request.get("coap://localhost:5683/path")
        self.assertEqual(r.code, codes.ok)

if __name__ == '__main__':
    unittest.main()
