# coding=utf-8
import unittest

from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.request import request
from pycolo.resource import Resource
from pycolo.codes import mediaCodes, codes, options


class DiscoveryResource(Resource):
    """
    CoRE Link Format

    This class implements the CoAP /.well-known/core resource.

    TD_COAP_LINK_01
    TD_COAP_LINK_02

    """

    DEFAULT_IDENTIFIER = ".well-known/core"

    #  The root resource of the endpoint used for recursive Link-Format generation. 
    root = Resource()

    def __init__(self, rootResource):
        self.contentType = mediaCodes.APPLICATION_LINK_FORMAT
        self.root = rootResource

    def performGET(self, request):
        response = Response(codes.RESP_CONTENT)  # create response
        query = request.options[options.URI_QUERY]  # get filter query
        #  return resources in link-format
        response.payload = Resource.toLink(self.root, query, True), mediaCodes.APPLICATION_LINK_FORMAT
        request.respond(response)  # complete the request

class DiscoveryTest(unittest.TestCase):

    def setUp(self):
        server = Endpoint()
        res = DiscoveryResource()
        server.register(res)

    def test_GET_wellKnown(self):
        """
        Identifier: TD_COAP_LINK_01
        Objective: Access to well-known interface for resource discovery
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports CoRE Link Format
            • Server supports /.well-known/core resource and the CoRE Link Format

        Step 1 (stimulus) Client is requested retrieve Server’s list of resource

        Step 2 (check (CON)) Client sends a GET request to Server for /.well-known/core resource

        Step 3 (check (CON)) Server sends response containing:
            Content-Type option indicating 40 (application/link-format)
            payload indicating all the links available on Server

        Step 4 (verify (IOP)) Client displays the list of resources available on Server
        """
        r = request.get("coap://localhost:5683/.well-known/core")

    def test_GET_wellKnown_Filtered(self):
        """
        Identifier: TD_COAP_LINK_02
        Objective: Use filtered requests for limiting discovery results
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports CoRE Link Format
            • Server supports CoRE Link Format
            • Server offers different types of resources (Type1, Type2, ...; see Note)

        Step 1 stimulus Client is requested retrieve Server’s list of resource of a
        specific type Type1

        Step 2 (check (CON)) Client sends a GET request to Server for /.well-known/core
        resource containing URI-Query indicating “rt=Type1”

        Step 3 (check (CON)) Server sends response containing:
        Content-Type option indicating 40 (application/link-format)
        payload indicating only the links of type Type1 available on
        Server

        Step 4 (verify (IOP)) Client displays the list of resources of type Type1 available on
        Server

        Note: Type1, Type2, ... refer to real resource types available on Server and shall be extracted from Server’s
        /.well-known/core resource
        """
        pass

if __name__ == '__main__':
    unittest.main()
