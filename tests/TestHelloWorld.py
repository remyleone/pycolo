# coding=utf-8
import unittest
from pycolo import codes
from pycolo.codes import mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.request import request
from pycolo.resource import Resource

class HelloWorldResource(Resource):
    """
    This class implements a 'hello world' resource for demonstration purposes.
    Defines a resource that returns text with special characters on GET.
    """

    def __init__(self, title="Hello-World Resource", rt="HelloWorldDisplayer"):
        self.title = title
        self.resourceType = rt

    def performGET(self, request):
        # create response
        response = Response(code=codes.RESP_CONTENT)

        payload = "Hello World! My name is Rémy Léone look @ the funny € from UTF-8 (•‿•)"
        response.contentType(mediaCodes.text)
        response.payload = payload
        return response


class HelloWorldTest(unittest.TestCase):

    def setUp(self):
        server = Endpoint()
        res = HelloWorldResource()
        server.register(res)

    def test_GET(self):
        r = request.get("coap://localhost:5683/.well-known/core")
        self.assertEqual(codes.ok, r.code)
        self.assertEqual(r.payload, "Hello World! My name is Rémy Léone look @ the funny €")


if __name__ == '__main__':
    unittest.main()
