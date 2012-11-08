# coding=utf-8
import unittest

from pycolo.codes import codes
from pycolo.codes import mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.request import request
from pycolo.resource import Resource


class DefaultResource(Resource):
    """
    This resource implements a test of specification for the
    ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.

    TD_COAP_CORE_01
    TD_COAP_CORE_02
    TD_COAP_CORE_03
    TD_COAP_CORE_04
    TD_COAP_CORE_05
    TD_COAP_CORE_06
    TD_COAP_CORE_07
    TD_COAP_CORE_08
    TD_COAP_CORE_10
    TD_COAP_CORE_11
    TD_COAP_CORE_14
    """

    def __init__(self):
        self.title = "Default test resource"
        self.name = "/test"

    def performGET(self, request):
        response = Response(codes.RESP_CONTENT)

        payload = str(request)

        if request.getToken().length > 0:
            payload.append("Token: ")
            payload.append(request.getTokenString())

        if len(payload) > 64:
            payload.delete(62, len(payload))
            payload.append('>>')

        response.payload = payload  # set payload
        response.contentType = mediaCodes.text
        request.respond(response)  # complete the request

    def performPOST(self, request):
        response = Response(codes.RESP_CREATED)

        payload = dict()
        payload["type"] = request.type
        payload["code"] = request.code
        payload["Message ID"] = request.MID
        payload["Content Type"] = request.contentType
        payload["Size"] = request.payloadSize

        if request.getToken():
            payload["Token String"] = request.getTokenString()

        if len(str(payload)) > 64:
            payload.delete(62, len(payload))
            payload.append('>>')

        response.payload = str(payload)
        response.contentType = mediaCodes.text
        response.path = "/nirvana"
        request.respond(response)  # complete the request

    def performPUT(self, request):
        response = Response(codes.RESP_CHANGED)

        payload = str(request)

        if request.getToken().length > 0:
            payload.append("\nTo: ")
            payload.append(request.getTokenString())

        if len(payload) > 64:
            payload.delete(62, len(payload))
            payload.append('>>')

        response.payload = str(payload)
        response.contentType = mediaCodes.text
        request.respond(response)  # complete the request


    def performDELETE(self, request):
        response = Response(codes.RESP_DELETED)

        payload = str(request)
        if request.token:
            payload.append("Token: ")
            payload.append(request.getTokenString())

        if len(payload) > 64:
            payload.delete(62, len(payload))
            payload.append('>>')

        response.payload = payload
        response.contentType = mediaCodes.text
        request.respond(response)  # complete the request


class TestDefault(unittest.TestCase):
    def setUp(self):
        server = Endpoint()
        res = DefaultResource()
        server.register(res)

    def test_GET(self):
        """
        Identifier: TD_COAP_CORE_01
        Objective: Perform GET transaction (CON mode)
        Configuration: CoAP_CFG_01
        Pre-test conditions: Server offers the resource /test that handle GET with an arbitrary payload

        # Step 1 (stimulus): Client is requested to send a GET request with:
        # • Type = 0(CON)
        # • Code = 1(GET)
        # Step 2 (check): Sent request contains Type value indicating 0 and Code value indicating 1
        # Step 3 (check): Server sends response containing:
        # • Code = 69(2.05 Content)
        # • The same Message ID as that of the previous request
        # • Content type option
        # Step 4 (verify): Client displays the received information
        """
        r = request.get("localhost:5683/")
        self.assertEqual(codes.content, r.code)

    def test_POST(self):
        """
        Identifier: TD_COAP_CORE_02
        Objective: Perform POST transaction (CON mode)
        Configuration: CoAP_CFG_01
        Pre-test conditions: Server accepts creation of new resource on /test (resource does not exists yet)

        Step 1 (stimulus) Client is requested to send a POST request with:
            • Type = 0(CON)
            • Code = 2(POST)
            • An arbitrary payload
            • Content type option

        Step 2 (check (CON)) Sent request contains Type value indicating 0 and Code value
        indicating 2

        Step 3 (verify (IOP)) Server displays received information

        Step 4 (check (CON)) Server sends response containing:
            • Code = 65(2.01 Created)
            • The same Message ID as that of the previous request

        Step 5 (verify (IOP)) Client displays the received response
        """

        r = request.post("localhost:5683/")
        self.assertEqual(codes.ok, r.code)

    def test_PUT(self):
        """
        Identifier: TD_COAP_CORE_03
        Objective: Perform PUT transaction (CON mode)
        Configuration: CoAP_CFG_01

        Step 1 (stimulus) Client is requested to send a PUT request with:
            • Type = 0(CON)
            • Code = 3(PUT)
            • An arbitrary payload
            • Content type option

        Step 2 (check (CON)) Sent request contains Type value indicating 0 and Code value indicating 3

        Step 3 (verify (IOP)) Server displays received information

        Step 4 (check (CON)) Server sends response containing:
            • Code = 68(2.04 Changed)
            • The same Message ID as that of the previous request

        Step 5 (verify (IOP)) Client displays the received response
        """
        r = request.put("localhost:5683")
        self.assertEqual(codes.ok, r.code)


    def test_DELETE(self):
        """
        Identifier: TD_COAP_CORE_04
        Objective: Perform DELETE transaction (CON mode)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a /test resource that handles DELETE

        Step 1 (stimulus) Client is requested to send a DELETE request with:
            • Type = 0(CON)
            • Code = 4(DELETE)

        Step 2 (check (CON)) Sent request contains Type value indicating 0 and Code value indicating 4

        Step 3 (check (CON)) Server sends response containing:
            • Code = 66(2.02 Deleted)
            • The same Message ID as that of the previous request

        Step 4 (verify (IOP)) Client displays the received information
        """
        r = request.delete("localhost:5683")
        self.assertEqual(codes.ok, r.code)


    def test_GET_NON(self):
        """
        Identifier: TD_COAP_CORE_05
        Objective: Perform GET transaction (NON mode)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a /test resource that handles GET

        Step 1 (stimulus) Client is requested to send a GET request with:
            • Type = 1(NON)
            • Code = 1(GET)

        Step 2 (check (CON)) Sent request contains Type value indicating 1 and Code value indicating 1

        Step 3 (check (CON)) Server sends response containing:
            • Type = 1(NON)
            • Code= 69(2.05 Content)
            • Content type option

        Step 4 (verify (IOP)) Client displays the received information
        """
        pass

    def test_POST_NON(self):
        """
        Identifier: TD_COAP_CORE_06
        Objective: Perform POST transaction (NON mode)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server accepts creation of new resource on /test (resource does not exists yet)

        Step 1 (stimulus) Client is requested to send a POST request with:
            • Type = 1(NON)
            • Code = 2(POST)
            • An arbitrary payload
            • Content type option

        Step 2 check (CON) Sent request contains Type value indicating 1 and Code value indicating 2

        Step 3 (verify) Server displays the received information

        Step 4 (check (CON)) Server sends response containing:
            • Type = 1(NON)
            • Code = 65(2.01 Created)

        Step 5 (verify (IOP)) Client displays the received response
        """
        pass

    def test_PUT_non(self):
        """
        Identifier: TD_COAP_CORE_07
        Objective: Perform PUT transaction (NON mode)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a /test resource that handles PUT

        Step 1 stimulus Client is requested to send a PUT request with:
            • Type = 1(NON)
            • Code = 3(PUT)
            • An arbitrary payload
            • Content type option

        Step 2 (check (CON)) Sent request contains Type value indicating 1 and Code value indicating 3

        Step 3 verify Server displays the received information

        Step 4 (check (CON)) Server sends response containing:
            • Type = 1(NON)
            • Code = 68(2.04 Changed)

        Step 5 (verify (IOP)) Client displays the received response
        """
        pass

    def test_DELETE_non(self):
        """
        Identifier: TD_COAP_CORE_08
        Objective: Perform DELETE transaction (NON mode)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a /test resource that handles DELETE

        Step 1 stimulus Client is requested to send a DELETE request with:
            • Type = 1(NON)
            • Code = 4(DELETE)

        Step 2 (check (CON)) Sent request contains Type value indicating 1 and Code value indicating 4

        Step 3 (check (CON)) Server sends response containing:
            • Type = 1(NON)
            • Code = 66(2.02 Deleted)

        Step 4 (verify (IOP)) Client displays the received information
        """
        pass

    def test_GET_Token(self):
        """
        Identifier: TD_COAP_CORE_10
        Objective: Handle request containing Token option
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a /test resource that handles GET

        Step 1 stimulus Client is requested to send a GET request to server’s
        resource including Token option

        Step 2 (Check (CON)) Sent request must contain:
            • Type = 0 (CON)
            • Code = 1 (GET)
            • Client generated Token value
            • Length of the token should be between 1 to 8 B
            • Option Type = Token

        Step 3 (Check (CON)) Server sends response containing:
            • Code = 69 (2.05 content)
            • Length of the token should be between 1 to 8 B
            • Token value same as the requested
            • Payload = Content of the requested resource
            • Content type option

        Step 4 (Verify (IOP)) Client displays the response
        """
        pass

    def test_GET_NoToken(self):
        """
        Identifier: TD_COAP_CORE_11
        Objective: Handle request not containing Token option
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a /test resource that handles GET

        Step 1 stimulus Client is requested to send a confirmable GET request to server’s resource not containg Token option

        Step 2 (Check (CON)) Sent request must contain:
            • Type = 0 (CON)
            • Code = 1 (GET)
            • No Token option

        Step 3 (Check (CON)) Server sends response containing:
            • Code = 69 (2.05 content)
            • No Token option
            • Payload = Content of the requested resource
            • Content type option

        Step 4 (Verify (IOP)) Client displays the response
        """
        pass

    def test_GET_lossy(self):
        """
        Identifier: TD_COAP_CORE_14
        Objective: Interoperate in lossy context (CON mode, piggybacked response)
        Configuration: CoAP_CFG_02

        Pre-test conditions:
            • Gateway is introduced and configured to produce packet loss
            • Server offers a /test resource that can handle GET

        Need to observe :
            • One dropped request
            • One dropped request ACK
            • One dropped response
            • One dropped response ACK and its retransmission
            • Test sequence should be executed several times

        Step 1 stimulus Client is requested to send a confirmable GET request to server’s resource

        Step 2 (Check (CON)) Sent request must contain:
            • Type = 0
            • Code = 1
            • Client generated Message ID

        Step 3 (Check (CON)) Server sends response containing:
            • Type = 2 (ACK)
            • Code = 69 (2.05 content)
            • Payload = Content of the requested resource
            • Content type option

        Step 4 (Verify (IOP)) Client displays the response
        """
        pass


    def test_GET_separate_lossy(self):
        """
        Identifier: TD_COAP_CORE_15
        Objective: Interoperate in lossy context (CON mode, delayed response)
        Configuration: CoAP_CFG_02

        Pre-test conditions:
            • Gateway is introduced and configured to produce packet loss
            • Server offers a /separate resource which cannot be served immediately and which
              cannot be acknowledged in a piggy-backed way.

        Need to observe :
            • One dropped request
            • One dropped request ACK
            • One dropped response
            • One dropped response ACK and its retransmission
            • Test sequence should be executed several times

        Step 1 (stimulus) Client is requested to send a confirmable GET request to server’s resource

        Step 2 (Check (CON)) Sent request must contain:
            • Type = 0
            • Code = 1
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


    def test_GET_separate(self):
        """
        Identifier: TD_COAP_CORE_16
        Objective: Perform  GET transaction with a separate response (NON mode)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Server offers a resource /separate which cannot be served immediately.

        Step 1 stimulus Client is requested to send a confirmable GET request to server’s resource

        Step 2 (Check (CON)) Sent request must contain:
            • Type = 1 (NON)
            • Code = 1 (GET)
            • Client generated Message ID

        Step 3 (Check (CON)) Server does not send response containing:
            • Type = 2 (ACK)
            • message ID same as the request
            • empty Payload

        Step 4 (Check (CON)) Server sends response containing:
            • Type  = 1 (NON)
            • Code = 69 (2.05 content)
            • Payload = Content of the requested resource
            • Content type option

        Step 5 (Verify (IOP)) Client displays the response
        """
        pass


if __name__ == '__main__':
    unittest.main()
