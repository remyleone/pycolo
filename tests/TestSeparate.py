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

if __name__ == '__main__':
    unittest.main()
