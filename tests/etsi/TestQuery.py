# coding=utf-8

"""
TODO
"""

import unittest
from pycolo.endpoint import Endpoint
from pycolo.resource import Resource

class Query(Resource):
    """
    Resource accepting query parameters

    This resource implements a test of specification for the
    ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.

    TD_COAP_CORE_13
    """

    def __init__(self):
        self.title = "Resource accepting query parameters"
        self.name = "/query"

    def performGET(self, request):
        """

        :param request:
        """
        pass

    #
#        response = Response(codes.RESP_CONTENT)  # create response
#
#        payload = "Type: %d (%s)\nCode: %d (%s)\nMID: %d" %\
#                  request.getType().ordinal(),\
#                  request.typeString,\
#                  request.code,\
#                  request.MID
#
#        for (Option query : request.getOptions(OptionNumberRegistry.URI_QUERY)):
#        String keyValue[] = query.getStringValue().split("=")
#
#        payload.append("Query: " + keyValue[0])
#
#        if keyValue.length == 2:
#            payload.append(": ")
#            payload.append(keyValue[1])
#
#        if len(payload) > 64:
#            payload.delete(62, len(payload))
#            payload.append('>>')
#
#        response.payload = str(payload)  # set payload
#        response.contentType = mediaCodes.text
#        request.respond(response)  # complete the request


class TestQuery(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        res = Query()
        server = Endpoint()
        server.addResource(res)

    def test_query_options(self):
        """
        Identifier: TD_COAP_CORE_13
        Objective: Handle request containing several URI-Query options
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a /query resource

        Step 1 stimulus Client is requested to send a confirmable GET request with
        three Query parameters (e.g. ?first=1&second=2&third=3) to
        the server’s resource

        Step 2 (Check (CON)) Sent request must contain:
            • Type = 0 (CON)
            • Code = 1 (GET)
            • Option type = URI-Query (More than one query parameter)

        Step 3 (Check (CON)) Server sends response containing:
            • Type = 0/2 (CON/ACK)
            • Code = 69 (2.05 content)
            • Payload = Content of the requested resource
            • Content type option

        Step 4 (Verify (IOP)) Client displays the response
        """
        pass

if __name__ == '__main__':
    unittest.main()
