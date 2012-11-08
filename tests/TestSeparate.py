# coding=utf-8
import time

import unittest
from pycolo.codes import codes
from pycolo.codes import mediaCodes
from pycolo.message import Response
from pycolo.resource import Resource


class Separate(Resource):
    """
    This class implements a 'separate' resource for demonstration purposes.
    Defines a resource that returns a response in a separate CoAP Message
    """

    def __init__(self):
        self.title = "Resource which cannot be served immediately and which\
             cannot be acknowledged in a piggy-backed way"
        self.resourceType = "SepararateResponseTester"
        self.name = "/separate"

    def performGET(self, request):
        """
        we know this stuff may take longer...
        promise the client that this request will be acted upon
        by sending an Acknowledgement
        :param request:
        :return:
        """
        request.accept()
        time.sleep(1)  # do the time-consuming computation

        response = Response(codes.RESP_CONTENT)  # create response
        #  set payload
        payload = dict()
        payload["type"] = request.type.ordinal()
        payload["type-string"] = request.typeString()
        payload["Code"] = request.code
        payload["Message ID"] = request.MID
        response.payload = str(payload)
        response.contentType = mediaCodes.text
        request.respond(response)  # complete the request


class TestSeparate(unittest.TestCase):
    def setUp(self):
        sep = Separate()

    def test_GET_separate(self):
        """
        Identifier: TD_COAP_CORE_09
        Objective: Perform  GET transaction with a separate response
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a resource /separate which cannot be served immediately and which
              cannot be acknowledged in a piggy-backed way.

        Step 1 stimulus Client is requested to send a confirmable GET request to server’s resource

        Step 2 (Check (CON)) Sent request must contain:
            • Type = 0 (CON)
            • Code = 1 (GET)
            • Client generated Message ID

        Step 3 (Check (CON)) Server sends response containing:
            • Type = 2 (ACK)
            • message ID same as the request
            • empty Payload

        Step 4 (Check (CON)) Server sends response containing:
            • Type  = 0 (CON)
            • Code = 69 (2.05 content)
            • Payload = Content of the requested resource
            • Content type option

        Step 5 (Check (CON)) Client sends response containing:
            • Type = 2 (ACK)
            • message ID same as the response
            • empty Payload

        Step 6 (Verify (IOP)) Client displays the response
        """
        pass

if __name__ == '__main__':
    unittest.main()
