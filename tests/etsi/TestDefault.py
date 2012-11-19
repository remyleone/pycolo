# coding=utf-8

"""
TODO
"""

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

    - TD_COAP_CORE_01
    - TD_COAP_CORE_02
    - TD_COAP_CORE_03
    - TD_COAP_CORE_04
    - TD_COAP_CORE_05
    - TD_COAP_CORE_06
    - TD_COAP_CORE_07
    - TD_COAP_CORE_08
    - TD_COAP_CORE_10
    - TD_COAP_CORE_11
    - TD_COAP_CORE_14
    """

    def __init__(self):
        self.title = "Default test resource"
        self.name = "/test"

    def performGET(self, request):
        """

        :param request:
        """
        response = Response(codes.RESP_CONTENT)

        payload = str(request)

        if request.getToken().length > 0:
            payload += "Token: "
            payload += request.getTokenString()

        if len(payload) > 64:
            payload.delete(62, len(payload))
            payload += '>>'

        response.payload = payload  # set payload
        response.contentType = mediaCodes.text
        request.respond(response)  # complete the request

    def performPOST(self, request):
        """

        :param request:
        """
        response = Response(codes.RESP_CREATED)

        payload = {"type": request.type,
                   "code": request.code,
                   "Message ID": request.MID,
                   "Content Type": request.contentType,
                   "Size": request.payloadSize}

        if request.getToken():
            payload["Token String"] = request.getTokenString()

        if len(str(payload)) > 64:
            payload.delete(62, len(payload))
            payload += '>>'

        response.payload = str(payload)
        response.contentType = mediaCodes.text
        response.path = "/nirvana"
        request.respond(response)  # complete the request

    def performPUT(self, request):
        """

        :param request:
        """
        response = Response(codes.RESP_CHANGED)

        payload = str(request)

        if request.getToken().length > 0:
            payload += "\nTo: "
            payload += request.getTokenString()

        if len(payload) > 64:
            payload.delete(62, len(payload))
            payload += '>>'

        response.payload = str(payload)
        response.contentType = mediaCodes.text
        request.respond(response)  # complete the request


    def performDELETE(self, request):
        """

        :param request:
        """
        response = Response(codes.RESP_DELETED)

        payload = str(request)
        if request.token:
            payload += "Token: "
            payload += request.getTokenString()

        if len(payload) > 64:
            payload.delete(62, len(payload))
            payload += '>>'

        response.payload = payload
        response.contentType = mediaCodes.text
        request.respond(response)  # complete the request


class TestDefault(unittest.TestCase):
    """
    TODO
    """
    def setUp(self):
        """
        TODO
        """
        server = Endpoint()
        res = DefaultResource()
        server.register(res)

    def test_TD_COAP_CORE_01(self):
        """
        :Identifier: TD_COAP_CORE_01
        :Objective: Perform GET transaction (CON mode)
        :Configuration: CoAP_CFG_01
        :Pre-test conditions: Server offers the resource /test that handle GET with an arbitrary payload

        Step 1 (stimulus): Client is requested to send a GET request with:
            - Type = 0(CON)
            - Code = 1(GET)

        Step 2 (check): Sent request contains Type value indicating 0 and Code value indicating 1

        Step 3 (check): Server sends response containing:
            • Code = 69(2.05 Content)
            • The same Message ID as that of the previous request
            • Content type option

        Step 4 (verify): Client displays the received information
        """
        r = request.get("localhost:5683/")
        self.assertEqual(codes.content, r.code)

    def test_TD_COAP_CORE_02(self):
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

    def test_TD_COAP_CORE_03(self):
        """
        :Identifier: TD_COAP_CORE_03
        :Objective: Perform PUT transaction (CON mode)
        :Configuration: CoAP_CFG_01

        - Step 1 (stimulus) Client is requested to send a PUT request with:
            - Type = 0(CON)
            - Code = 3(PUT)
            - An arbitrary payload
            - Content type option

        - Step 2 (check (CON)) Sent request contains Type value indicating 0 and Code value indicating 3

        - Step 3 (verify (IOP)) Server displays received information

        - Step 4 (check (CON)) Server sends response containing:
            - Code = 68(2.04 Changed)
            - The same Message ID as that of the previous request

        - Step 5 (verify (IOP)) Client displays the received response
        """
        r = request.put("localhost:5683")
        self.assertEqual(codes.ok, r.code)


    def test_TD_COAP_CORE_04(self):
        """
        :Identifier: TD_COAP_CORE_04
        :Objective: Perform DELETE transaction (CON mode)
        :Configuration: CoAP_CFG_01

        Pre-test conditions:
            - Server offers a /test resource that handles DELETE

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


    def test_TD_COAP_CORE_05(self):
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

    def test_TD_COAP_CORE_06(self):
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

    def test_TD_COAP_CORE_07(self):
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

    def test_TD_COAP_CORE_08(self):
        """
        Identifier: TD_COAP_CORE_08
        Objective: Perform DELETE transaction (NON mode)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            - Server offers a /test resource that handles DELETE

        Step 1 stimulus Client is requested to send a DELETE request with:
            - Type = 1(NON)
            - Code = 4(DELETE)

        Step 2 (check (CON)) Sent request contains Type value indicating 1 and Code value indicating 4

        Step 3 (check (CON)) Server sends response containing:
            - Type = 1(NON)
            - Code = 66(2.02 Deleted)

        Step 4 (verify (IOP)) Client displays the received information
        """
        pass

    def test_TD_COAP_CORE_10(self):
        """
        Identifier: TD_COAP_CORE_10
        Objective: Handle request containing Token option
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            - Server offers a /test resource that handles GET

        Step 1 stimulus Client is requested to send a GET request to server’s
        resource including Token option

        Step 2 (Check (CON)) Sent request must contain:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - Client generated Token value
            - Length of the token should be between 1 to 8 B
            - Option Type = Token

        Step 3 (Check (CON)) Server sends response containing:
            - Code = 69 (2.05 content)
            - Length of the token should be between 1 to 8 B
            - Token value same as the requested
            - Payload = Content of the requested resource
            - Content type option

        Step 4 (Verify (IOP)) Client displays the response
        """
        pass

    def test_TD_COAP_CORE_11(self):
        """
        :Identifier: TD_COAP_CORE_11
        :Objective: Handle request not containing Token option
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server offers a /test resource that handles GET

        - Step 1 stimulus Client is requested to send a confirmable GET request to server’s resource not containg Token option

        - Step 2 (Check (CON)) Sent request must contain:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - No Token option

        - Step 3 (Check (CON)) Server sends response containing:
            - Code = 69 (2.05 content)
            - No Token option
            - Payload = Content of the requested resource
            - Content type option

        - Step 4 (Verify (IOP)) Client displays the response
        """
        pass

    def test_TD_COAP_CORE_14(self):
        """
        :Identifier: TD_COAP_CORE_14
        :Objective: Interoperate in lossy context (CON mode, piggybacked response)
        :Configuration: CoAP_CFG_02

        :Pre-test conditions:
            - Gateway is introduced and configured to produce packet loss
            - Server offers a /test resource that can handle GET

        Need to observe :
            - One dropped request
            - One dropped request ACK
            - One dropped response
            - One dropped response ACK and its retransmission
            - Test sequence should be executed several times

        - Step 1 stimulus Client is requested to send a confirmable GET request to server’s resource

        - Step 2 (Check (CON)) Sent request must contain:
            - Type = 0
            - Code = 1
            - Client generated Message ID

        - Step 3 (Check (CON)) Server sends response containing:
            - Type = 2 (ACK)
            - Code = 69 (2.05 content)
            - Payload = Content of the requested resource
            - Content type option

        - Step 4 (Verify (IOP)) Client displays the response
        """
        pass


    def test_TD_COAP_CORE_15(self):
        """
        :Identifier: TD_COAP_CORE_15
        :Objective: Interoperate in lossy context (CON mode, delayed response)
        :Configuration: CoAP_CFG_02

        :Pre-test conditions:
            - Gateway is introduced and configured to produce packet loss
            - Server offers a /separate resource which cannot be served immediately and which
              cannot be acknowledged in a piggy-backed way.

        :Need to observe:
            - One dropped request
            - One dropped request ACK
            - One dropped response
            - One dropped response ACK and its retransmission
            - Test sequence should be executed several times

        - Step 1 (stimulus) Client is requested to send a confirmable GET request to server’s resource

        - Step 2 (Check (CON)) Sent request must contain:
            - Type = 0
            - Code = 1
            - Client generated Message ID

        - Step 3 (Check (CON)) Server sends response containing:
            - Type = 2 (ACK)
            - message ID same as the request
            - empty Payload

        - Step 4 (Check (CON)) Server sends response containing:
            - Type  = 0 (CON)
            - Code = 69 (2.05 content)
            - Payload = Content of the requested resource
            - Content type option

        - Step 5 (Check (CON)) Client sends response containing:
            - Type = 2 (ACK)
            - message ID same as the response
            - empty Payload

        - Step 6 (Verify (IOP)) Client displays the response
        """
        pass


    def test_TD_COAP_CORE_16(self):
        """
        :Identifier: TD_COAP_CORE_16
        :Objective: Perform  GET transaction with a separate response (NON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server offers a resource /separate which cannot be served immediately.

        - Step 1 stimulus Client is requested to send a confirmable GET request to server’s resource

        - Step 2 (Check (CON)) Sent request must contain:
            - Type = 1 (NON)
            - Code = 1 (GET)
            - Client generated Message ID

        - Step 3 (Check (CON)) Server does not send response containing:
            - Type = 2 (ACK)
            - message ID same as the request
            - empty Payload

        - Step 4 (Check (CON)) Server sends response containing:
            - Type  = 1 (NON)
            - Code = 69 (2.05 content)
            - Payload = Content of the requested resource
            - Content type option

        - Step 5 (Verify (IOP)) Client displays the response
        """
        pass

    def test_TD_COAP_CORE_18(self):
        """
        :Identifier: TD_COAP_CORE_18
        :Objective: Perform POST transaction with responses containing several Location-Path options (CON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server accepts creation of new resource on /test and the created resource is
                located at /location1/location2/location3 (resource does not exist yet)

        - Step 1 (Stimulus) Client is requested to send a confirmable POST request to server’s resource

        - Step 2 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 2 (POST)
            - An arbitrary payload
            - Content-format option

        - Step 3 (check) Server sends response containing:
            - Code = 65 (2.01 created)
            - Option type = Location-Path (one for each segment)
            - Option values must contain “location1”, “location2” &
                “location3” without containing any ‘/’

        - Step 4 (verify) Client displays the response
        """
        pass

    def test_TD_COAP_CORE_19(self):
        """
        :Identifier: TD_COAP_CORE_19
        :Objective: Perform POST transaction with responses containing several Location-Query options (CON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions: Server accepts creation of new resource on uri /location-query, the location of
            the created resource contains two query parameters ?first=1&second=2

        - Step 1 (stimulus) Client is requested to send a confirmable POST request to server’s resource

        - Step 2 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 2 (POST)
            - An arbitrary payload
            - Content-format option

        - Step 3 (check) Server sends response containing:
            - Code = 65 (2.01 created)
            - Two options whose type is Location-Query:
                - The first option contains first=1
                - The second option contains second=2

        - Step 4 (verify) Client displays the response
        """
        pass

    def test_TD_COAP_CORE_20(self):
        """
        :Identifier: TD_COAP_CORE_20
        :Objective: Perform GET transaction containing the Accept option (CON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions: Server should provide a resource /multi-format which exists in two formats:
            - text/plain;charset=utf-8
            - application/xml

        **Part A** Client requests a resource in text format

        - Step 1 (stimulus) Client is requested to send a confirmable GET request to server’s resource

        - Step 2 (check) The request sent request by the client contains:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - Option: type = Accept, value = 1 (text/plain;charset=utf-8)

        - Step 3 (check) Server sends response containing:
            - Code = 69 (2.05 content)
            - Option type = Content-Format, value = 1 (text/plain;charset=utf-8)
            - Payload = Content of the requested resource in text/plain;charset=utf-8 format

        - Step 4 (verify) Client displays the response

        **Part B** Client requests a resource in xml format

        - Step 5 (stimulus) Client is requested to send a confirmable GET request to server’s resource

        - Step 6 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - Option: type = Accept, value = 41 (application/xml)

        - Step 7 (check) Server sends response containing:
            - Code = 69 (2.05 content)
            - Option: type = Content-Format, value = 41 (application/xml)
            - Payload: Content of the requested resource in application/xml format

        - Step 8 : Client displays the response
        """
        pass

    def test_TD_COAP_CORE_21(self):
        """
        :Identifier: TD_COAP_CORE_21
        :Objective: Perform GET transaction containing the ETag option (CON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server should offer a /test resource which vary in time
            - Client & server supports ETag option
            - The Client ‘s cache must be purged

        **Part A** Verifying that client cache is empty

        - Step 1 (stimulus) Client is requested to send a confirmable GET request to server’s resource

        - Step 2 (check) The request sent request by the client contains:
            - Type = 0 (CON)
            - Code = 1 (GET)

        - Step 3 (check) Server sends response containing:
            - Code = 69 (2.05 content)
            - Option type = ETag
            - Option value = an arbitrary ETag value

        - Step 4 (verify) Client displays the response

        **Part B** Verifying client cache entry is still valid

        - Step 5 (stimulus) Client is requested to send s confirmable GET request to
            server’s resource so as to check if the resource was updated

        - Step 6 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - Option Type = ETag
            - Option value=the ETag value received in step 3

        - Step 7 (check) Server sends response containing:
            - Code = 67 (2.03 Valid)
            - Option type = ETag
            - Option value = the ETag value sent in step 3

        - Step 8 (verify) Client displays the response

        **Part C** Verifying that client cache entry is no longer valid

        - Step 9 (stimulus) Update the content of the server’s resource (either locally or from another CoAP client)

        - Step 10 (stimulus) Client is requested to send a confirmable GET request to
            server’s resource so as to check if the resource was updated

        - Step 11 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - Option Type=ETag
            - Option value=the ETag value received in step 3

        - Step 12 (check) Server sends response containing:
            - Code = 69 (2.05 Content)
            - Option type = ETag
            - Option value = an arbitrary ETag value which differs from the ETag sent in step 3

        - Step 13 (verify) Client displays the response
        """
        pass

    def test_TD_COAP_CORE_22(self):
        """
        :Identifier: TD_COAP_CORE_22
        :Objective: Perform GET transaction with responses containing the ETag option and requests
            containing the If-Match option (CON mode)
        :Configuration: CoAP_CFG_01
        :Pre-test conditions:
            - Server should offer a /test resource
            - Client & server supports ETag and If-Match option
            - The Client ‘s cache must be purged

        *Preamble* client gets the resource
        - Step 1 (stimulus) Client is requested to send a confirmable GET request to server’s resource

        - Step 2 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 1 (GET)

        - Step 3 (check) Server sends response containing:
            - Code = 69 (2.05 content)
            - Option type = ETag
            - Option value = an arbitrary Etag value
            - The payload

        *Part A* single update

        - Step 4 (Stimulus) Client is requested to send a confirmable PUT request to
            server’s resource so as to perform an atomic update

        - Step 5 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-Match
            - Option value=ETag value received in step 3
            - An arbitrary payload (which differs from the payload received in step 3)

        - Step 6 (check) Server sends response containing:
            - Code = 68 (2.04 Changed)
            - Option type = ETag
            - Option value = an arbitrary ETag value which differs from the ETag sent in step 3

        - Step 7 (verify) Client displays the response and the server changed its resource

        *Part B* concurrent updates

        - Step 8 (stimulus) Update the content of the server’s resource (either locally or from another CoAP client)

        - Step 9 (stimulus) Client is requested to send a confirmable PUT request to server’s resource so as to
            perform an atomic update

        - Step 10 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-Match
            - Option value=ETag value received in step 6
            - An arbitrary payload (which differs from the previous payloads)

        - Step 11 (check) Server sends response containing:
            - Code = 140 (4.12 Precondition Failed)

        - Step 12 (verify) Client displays the response and the server did not update the
            content of the resource
        """
        pass

    def test_TD_COAP_CORE_23(self):
        """
        :Identifier: TD_COAP_CORE_23
        :Objective: Perform GET transaction with responses containing the ETag option and requests containing the
            If-None-Match option (CON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server should offer a /test resource, which does not exist and which can be created by the client
            - Client & server supports If-Non-Match

        *Part A* single creation

        - Step 1 (stimulus) Client is requested to send a confirmable PUT request to server’s resource so as to
            atomically create the resource.

        - Step 2 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-None-Match
            - An arbitrary payload

        - Step 3 (check) Server sends response containing:
            - Code = 65 (2.01 Created)

        - Step 4 (verify) Client displays the response and the server created a new resource

        *Part B* concurrent creations

        - Step 5 (stimulus) Client is requested to send a confirmable PUT request to server’s resource so as
            to atomically create the resource.

        - Step 6 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-None-Match
            - An arbitrary payload

        - Step 7 (check) Server sends response containing:
            - 140 (4.12 Precondition Failed)


        - Step 8 (verify) Client displays the response
        """
        pass

    def test_TD_COAP_CORE_24(self):
        """
        :Identifier: TD_COAP_CORE_24
        :Objective: Perform POST transaction with responses containing several Location-Path options (Reverse
            Proxy in CON mode)

        :Configuration: CoAP_CFG_03

        :Pre-test conditions:
            - Proxy is configured as a reverse-proxy for the server
            - Proxy’s cache is cleared
            - Server accepts creation of new resource on /test and the created resource is
                located at /location1/location2/location3 (resource does not exist yet)

        - Step 1 (stimulus) Client is requested to send a confirmable POST request to proxy

        - Step 2 (check) The POST sent by the client contains:
            - Type = 0 (CON)
            - Code = 2 (POST)
            - An arbitrary payload
            - Content-format option

        - Step 3 (check) The Proxy forwards the POST request to server’s resource and that it contains:
            - Type = 0 (CON)
            - Code = 2 (POST)
            - An arbitrary payload
            - Content-format option

        - Step 4 (check) Server sends a response to the proxy containing:
            - Code = 65 (2.01 created)
            - Option type = Location-Path (one for each segment)
            - Option values must contain “location1”, “location2” & “location3” without contain any ‘/’

        - Step 5 (check) Observe that the Proxy forwards the response (in step 4) to client and check that the
            forwarded response contains:
            - Code = 65 (2.01 created)
            - Option type = Location-Path (one for each segment)
            - Option values must contain “location1”, “location2” & “location3” without contain any ‘/’

        - Step 6 (verify) Client displays the response

        - Step 7 (verify) Client interface returns the response
            - 2.01 created
            - Location: coap://proxy/location1/location2/location3
        """
        pass

    def test_TD_COAP_CORE_25(self):
        """
        :Identifier: TD_COAP_CORE_25
        :Objective: Perform POST transaction with responses containing several Location- Query option (Reverse proxy)
        :Configuration: CoAP_CFG_03

        :Pre-test conditions:
            - Proxy is configured as a reverse-proxy for the server
            - Proxy’s cache is cleared
            - Server accepts creation of new resource on uri /location-query, the location of
                the created resource contains two query parameters ?first=1&second=2

        - Step 1 (Stimulus): Client is requested to send a confirmable POST request to proxy

        - Step 2 (check) Proxy receives the request from client & forwards it to server’s resource

        - Step 3 (check) Forwarded request must contain:
            - Type = 0 (CON)
            - Code = 2 (POST)
            - An arbitrary payload
            - Content-format option

        - Step 4 (check) Server sends response to proxy containing:
            - Code = 65 (2.01 created)
            - Two options whose type is Location-Query
                - The first option contains first=1
                - The second option contains second=2

        - Step 5 (check) Proxy forwards the response to client

        - Step 6 (check) Client displays the message

        - Step 7 (verify) Client interface returns the response:
            - 2.01 created
            - Location: coap://proxy/?first=1&second=2
        """
        pass

    def test_TD_COAP_CORE_26(self):
        """
        :Identifier: TD_COAP_CORE_26
        :Objective: Perform GET transaction containing the Accept option (CON mode)
        :Configuration: CoAP_CFG_03

        :Pre-test conditions:
            - Proxy is configured as a reverse-proxy for the server
            - Proxy’s cache is cleared
            - Server should provide a resource /multi-format which exists in two formats:
                - text/plain;charset=utf-8
                - application/xml

        *Part A*: client requests text format

        - Step 1 (stimulus) Client is requested to send a confirmable GET request to proxy

        - Step 2 (check) Proxy receives the request from client & forwards it to server’s resource

        - Step 3 (check) Forwarded request must contain:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - Option: type = Accept, value = 1 (text/plain;charset=utf-8)

        - Step 4 (check) Server sends response containing:
            - Code = 69 (2.05 content)
            - Option: type = Content-Format, value = 1 (text/plain;charset=utf-8)
            - Payload = Content of the requested resource in text/plain;charset=utf-8 format

        - Step 5 (check) Proxy forwards the response to client

        - Step 6 (verify) Client receives & displays the response

        - Step 7 (check) Response contains:
            - Code = 69 (2.05 content)
            - Option: type = Content-Format, value = 1 (text/plain;charset=utf-8)
            - Payload = Content of the requested resource in text/plain;charset=utf-8 format

        *Part B*: client requests xml format

        - Step 8 (stimulus) Client is requested to send a confirmable GET request to Proxy

        - Step 9 (check) Proxy forwards the request to server

        - Step 10 (check) Sent request must contain:
            - Type = 0 (CON)
            - Code = 1 (GET)
                Option: type = Accept, value = 41 (application/xml)

        - Step 11 (check) Server sends response containing:
            - Code = 69 (2.05 content)
            - Option: type = Content-Format, value = 41 (application/xml)
            - Payload = Content of the requested resource in application/xml format

        - Step 12 (check) Proxy forwards the response to client

        - Step 13 (verify) Client receives & displays the response

        - Step 14 (check) Client displays the response received:
            - Code = 69 (2.05 content)
            - Option: type = Content-Format, value = 41 (application/xml)
            - Payload = Content of the requested resource in application/xml format

        """
        pass

    def test_TD_COAP_CORE_27(self):
        """
        :Identifier: TD_COAP_CORE_27
        :Objective: Perform GET transaction with responses containing the ETag option and requests containing the
            If-Match option (CON mode)
        :Configuration: CoAP_CFG_03

        :Pre-test conditions:
            - Proxy is configured as a reverse-proxy for the server
            - Proxy’s cache is cleared
            - Server should offer a /test resource
            - Client & server supports ETag option and If-Match option

        *Preamble* client gets the resource

        - Step 1 (stimulus) Client is requested to send a confirmable GET request to proxy

        - Step 2 (check) Proxy forwards the request to server

        - Step 3 (check) Forwarded request must contain:
            - Type = 0 (CON)
            - Code = 1 (GET)

        - Step 4 (check) Server sends response containing:
            - Code = 69 (2.05 content)
            - Option type = ETag
            - Option value = an arbitrary ETag value

        - Step 5 (check) Proxy forwards the response to client

        *Part A*: single update

        - Step 6 (stimulus) Client is requested to send a confirmable PUT request to Proxy

        - Step 7 (check) Sent request must contain:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-Match
            - Option value=ETag value received in step 4
            - An arbitrary payload (which differs from the payload received in step 3)

        - Step 8 (verify) Proxy forwards the request to servers resource & server updates the resource

        - Step 9 (check) Server sends response containing:
            - Code = 68 (2.04 Changed)
            - Option type = ETag
            - Option value = an arbitrary ETag value which differs from the ETag received in step 4

        - Step 10 (check) Proxy forwards the response to client

        - Step 11 (check) Forwarded response contains:
            - Code = 68 (2.04 Changed)
            - Option type = ETag
            - Option value = same ETag value found in step 8

        - Step 12 (verify) Client displays the response

        *Part B*: concurrent updates

        - Step 13 (stimulus) Update the content of the server’s resource (either locally or from another CoAP client)

        - Step 14 (stimulus) Client is requested to send s confirmable PUT request to proxy so as to perform an atomic update

        - Step 15 (check) Sent request must contain:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-Match
            - Option value=ETag value received in step 8
                An arbitrary payload (which differs from the previous payloads)

        - Step 16 (check) Proxy forwards the request to server’s resource

        - Step 17 (check) Sent request must contain:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-Match
            - Option value=same ETag value found in step 14 An arbitrary payload (which differs from the previous payloads)

        - Step 18 (check) Server sends response containing:
            - Code = 140 (4.12 Precondition Failed)

        - Step 19 (Verify) Proxy forwards the response to client

        - Step 20 (check) Response contains:
            - Code = 140 (4.12 Precondition Failed)

        - Step 21 (Verify) Client displays the response

        """
        pass

    def test_TD_COAP_CORE_28(self):
        """
        :Identifier: TD_COAP_CORE_28
        :Objective: Perform GET transaction with responses containing the ETag option and requests containing the
            If-None-Match option (CON mode) (Reverse proxy)
        :Configuration: CoAP_CFG_03

        :Pre-test conditions:
            - Proxy is configured as a reverse-proxy for the server
            - Proxy’s cache is cleared
            - Server should offer a /test resource, which does not exist and which can be created by the client
            - Client & server supports If-None-Match

        *Part A*: single creation

        - Step 1 (stimulus) Client is requested to send a confirmable PUT request to proxy to atomically create
            resource in server

        - Step 2 (check) Proxy forwards the request to server

        - Step 3 (check) Forwarded request must contain:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-None-Match
            - An arbitrary payload

        - Step 4 (check) Server sends response containing:
            - Code = 65 (2.01 Created)

        - Step 5 (check) Proxy forwards the response to client

        - Step 6 (verify) Client displays the response & and server created new resource

        *Part B*: concurrent creations

        - Step 5 (stimulus) Client is requested to send s confirmable PUT request to proxy to atomically create
            resource in server

        - Step 6 (check) Sent request must contain:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-Non-Match
            - Option value=Received ETag value

        - Step 7 (check) Server sends response containing:
            - 140 (4.12 Precondition Failed)

        - Step 8 (verify) Proxy forwards the response to client

        - Step 9 (check) Response contains:
            - 140 (4.12 Precondition Failed)

        - Step 10 (verify) Client displays the response
        """
        pass

    def test_TD_COAP_CORE_29(self):
        """
        :Identifier: TD_COAP_CORE_29
        :Objective: Perform GET transaction with responses containing the Max-Age option (Reverse proxy)
        :Configuration: CoAP_CFG_03

        :Pre-test conditions:
            - Proxy offers a cache
            - Proxy is configured as a reverse-proxy for the server
            - Servers resource vary in time and supports Max-Age option
            - Proxy’s cache is cleared
            - Server offers a resource /test that varies in time, with a Max-Age set to 30s

        - Step 1 (stimulus) A confirmable GET request is sent to Proxy from Client

        - Step 2 (check) Proxy Sends request containing:
            - Type = 0 (CON)
            - Code = 1 (GET)

        - Step 3 (check) Server sends response containing:
            - Code = 69 (2.05 Content)
            - Option type = ETag
            - Option value = ETag value
            - Option type = Max-age
            - Option value

        - Step 4 (verify) Proxy forwards response to client

        - Step 5 (stimulus) A confirmable GET request is sent to proxy from Client before Max-Age expires

        - Step 6 (check) Proxy dos not forward any request to the server

        - Step 7 (check) Proxy sends response to client

        - Step 8 (verify) Response contains:
            • Option type = Max-age
            • Option Value = new Max-age
            • Payload cached
        """
        pass

if __name__ == '__main__':
    unittest.main()
