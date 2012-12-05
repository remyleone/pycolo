# coding=utf-8

"""
Implementing ETSI CoAP CoRE Tests
"""
import logging

import unittest

from pycolo.codes import codes, msgType, options
from pycolo.codes import mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.request import request as coap
from pycolo.resource import Resource
from pycolo.token import acquireToken
from tests.etsi import Default, LongPath, Query, Separate
from tests.examples.TestProxy import Proxy


class TestCore(unittest.TestCase):
    """
    Test suite for ETSI CoAP Core Tests

    - TD_COAP_CORE_01 Perform GET transaction (CON mode)
    - TD_COAP_CORE_02 Perform POST transaction (CON mode)
    - TD_COAP_CORE_03 Perform PUT transaction (CON mode)
    - TD_COAP_CORE_04 Perform DELETE transaction (CON mode)
    - TD_COAP_CORE_05 Perform GET transaction (NON mode)
    - TD_COAP_CORE_06 Perform POST transaction (NON mode)
    - TD_COAP_CORE_07 Perform PUT transaction (NON mode)
    - TD_COAP_CORE_08 Perform DELETE transaction (NON mode)
    - TD_COAP_CORE_09 Perform GET transaction with delayed response (CON mode, no piggyback)
    - TD_COAP_CORE_10 Perform GET transaction containing Token option (CON mode)
    - TD_COAP_CORE_11 Perform GET transaction containing token option with a separate response (CON mode)
    - TD_COAP_CORE_12 Perform GET transaction not containing Token option (CON mode)
    - TD_COAP_CORE_13 Perform GET transaction containing several URI-Path options (CON mode)
    - TD_COAP_CORE_14 Perform GET transaction containing several URI-Query options (CON mode)
    - TD_COAP_CORE_17 Perform GET transaction with a separate response (NON mode)
    - TD_COAP_CORE_18 Perform POST transaction with responses containing several Location-Path options (CON mode)
    - TD_COAP_CORE_19 Perform POST transaction with responses containing several Location-Query options (CON mode)
    - TD_COAP_CORE_20 Perform GET transaction containing the Accept option (CON mode)
    - TD_COAP_CORE_21 Perform GET transaction containing the ETag option (CON mode)
    - TD_COAP_CORE_22 Perform GET transaction with responses containing the ETag option and requests containing the If-Match option (CON mode)
    - TD_COAP_CORE_23 Perform GET transaction with responses containing the ETag option and requests containing the If-None-Match option (CON mode)
    """

    def setUp(self):
        """
        TODO
        """
        server = Endpoint()
        res = Default()
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
            - Code = 69(2.05 Content)
            - The same Message ID as that of the previous request
            - Content type option

        Step 4 (verify): Client displays the received information
        """
        r = coap.get(self.server.url + "/test", confirmable=True,
            payload="TD_COAP_CORE_01",
            trace=True)
        self.assertEqual(r.sent.msgType, msgType.con)
        self.assertEqual(r.sent.code, codes.GET)
        self.assertEqual(r.code, codes.content)
        self.assertEqual(r.sent.messageID, r.messageID)
        self.assertEqual(r.sent.payload, r.payload)
        logging.info(r)

    def test_TD_COAP_CORE_02(self):
        """
        :Identifier: TD_COAP_CORE_02
        :Objective: Perform POST transaction (CON mode)
        :Configuration: CoAP_CFG_01
        :Pre-test conditions: Server accepts creation of new resource on /test (resource does not exists yet)

        - Step 1 (stimulus) Client is requested to send a POST request with:
            - Type = 0(CON)
            - Code = 2(POST)
            - An arbitrary payload
            - Content type option

        - Step 2 (check (CON)) Sent request contains Type value indicating 0 and Code value indicating 2

        - Step 3 (verify (IOP)) Server displays received information

        - Step 4 (check (CON)) Server sends response containing:
            - Code = 65(2.01 Created)
            - The same Message ID as that of the previous request

        - Step 5 (verify (IOP)) Client displays the received response
        """
        r = coap.post(self.server.url +  "/test", payload="TD_COAP_CORE_02")
        self.assertEqual(codes.ok, r.code)
        self.assertEqual(r.code, codes.created)
        self.assertEqual(r.msgType, msgType.ack)
        self.assertEqual(r.sent.MID, r.MID)
        logging.info(r)

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
        r = coap.put(self.server.url +  "/test",
            confirmable=True,
            payload="TD_COAP_CORE_02")
        self.assertEqual(codes.changed, r.code)
        self.assertEqual(r.msgType, msgType.ack)

    def test_TD_COAP_CORE_04(self):
        """
        :Identifier: TD_COAP_CORE_04
        :Objective: Perform DELETE transaction (CON mode)
        :Configuration: CoAP_CFG_01

        Pre-test conditions:
            - Server offers a /test resource that handles DELETE

        Step 1 (stimulus) Client is requested to send a DELETE request with:
            - Type = 0(CON)
            - Code = 4(DELETE)

        Step 2 (check (CON)) Sent request contains Type value indicating 0 and Code value indicating 4

        Step 3 (check (CON)) Server sends response containing:
            - Code = 66(2.02 Deleted)
            - The same Message ID as that of the previous request

        Step 4 (verify (IOP)) Client displays the received information
        """
        r = coap.delete(self.server.url + "/test")
        self.assertEqual(codes.deleted, r.code)
        self.assertEqual(r.msgType, msgType.ack)

    def test_TD_COAP_CORE_05(self):
        """
        :Identifier: TD_COAP_CORE_05
        :Objective: Perform GET transaction (NON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server offers a /test resource that handles GET

        - Step 1 (stimulus) Client is requested to send a GET request with:
            - Type = 1(NON)
            - Code = 1(GET)

        - Step 2 (check (CON)) Sent request contains Type value indicating 1 and Code value indicating 1

        - Step 3 (check (CON)) Server sends response containing:
            - Type = 1(NON)
            - Code= 69(2.05 Content)
            - Content type option

        - Step 4 (verify (IOP)) Client displays the received information
        """
        r = coap.get(self.server.url + "/test", confirmable=False)
        self.assertEqual(r.msgType, msgType.non)
        self.assertEqual(r.code, codes.content)
        self.assertIn("Content-Type", r)

    def test_TD_COAP_CORE_06(self):
        """
        :Identifier: TD_COAP_CORE_06
        :Objective: Perform POST transaction (NON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server accepts creation of new resource on /test (resource does not exists yet)

        - Step 1 (stimulus) Client is requested to send a POST request with:
            - Type = 1(NON)
            - Code = 2(POST)
            - An arbitrary payload
            - Content type option

        - Step 2 check (CON) Sent request contains Type value indicating 1 and Code value indicating 2

        - Step 3 (verify) Server displays the received information

        - Step 4 (check (CON)) Server sends response containing:
            - Type = 1(NON)
            - Code = 65(2.01 Created)

        - Step 5 (verify (IOP)) Client displays the received response
        """
        r = coap.post(self.server.url + "/test",
            confirmable=False, payload="TD_COAP_CORE_06")
        self.assertEqual(r.code, codes.created)
        self.assertEqual(r.msgType, msgType.non)

    def test_TD_COAP_CORE_07(self):
        """
        :Identifier: TD_COAP_CORE_07
        :Objective: Perform PUT transaction (NON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server offers a /test resource that handles PUT

        - Step 1 (stimulus) Client is requested to send a PUT request with:
            - Type = 1(NON)
            - Code = 3(PUT)
            - An arbitrary payload
            - Content type option

        - Step 2 (check (CON)) Sent request contains Type value indicating 1 and Code value indicating 3

        - Step 3 verify Server displays the received information

        - Step 4 (check (CON)) Server sends response containing:
            - Type = 1(NON)
            - Code = 68(2.04 Changed)

        - Step 5 (verify (IOP)) Client displays the received response
        """
        r = coap.put(self.server.url + "/test",
            confirmable=False, payload="TD_COAP_CORE_07")
        self.assertEqual(r.msgType, msgType.non)
        self.assertEqual(r.code, codes.changed)

    def test_TD_COAP_CORE_08(self):
        """
        :Identifier: TD_COAP_CORE_08
        :Objective: Perform DELETE transaction (NON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server offers a /test resource that handles DELETE

        - Step 1 stimulus Client is requested to send a DELETE request with:
            - Type = 1(NON)
            - Code = 4(DELETE)

        - Step 2 (check (CON)) Sent request contains Type value indicating 1 and Code value indicating 4

        - Step 3 (check (CON)) Server sends response containing:
            - Type = 1(NON)
            - Code = 66(2.02 Deleted)

        - Step 4 (verify (IOP)) Client displays the received information
        """
        r = coap.delete(self.server.url + "/test", confirmable=False)
        self.assertEqual(r.msgType, msgType.non)
        self.assertEqual(r.code, codes.deleted)

    def test_TD_COAP_CORE_09(self):
        """
        :Identifier: TD_COAP_CORE_09
        :Objective: Perform  GET transaction with a separate response
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server offers a resource /separate which cannot be served immediately and which
                cannot be acknowledged in a piggy-backed way.

        - Step 1 stimulus Client is requested to send a confirmable GET request to server’s resource

        - Step 2 (Check (CON)) Sent request must contain:
            - Type = 0 (CON)
            - Code = 1 (GET)
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
        r = coap.get(self.server.url + "/separate", confirmable=True)
        self.assertEqual(r.msgType, msgType.non)
        self.assertIn("Content-Type", r)
        self.assertEqual(r.code, codes.content)

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
        token = acquireToken()  # not preferring empty token
        r = coap.get(self.server.url + "/test", confirmable=True, token=token,
            trace=True)
        self.assertEqual(r.code, codes.content)
        self.assertEqual(r.msgType, msgType.ack)
        self.assertEqual(
            r.sent.options[options.token],
            r.options[options.token])
        self.assertIn("Content-Type", r)

    def test_TD_COAP_CORE_11(self):
        """
        :Identifier: TD_COAP_CORE_11
        :Objective: Handle request not containing Token option
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server offers a /test resource that handles GET

        - Step 1 stimulus Client is requested to send a confirmable GET
            request to server’s resource not containing Token option

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
        r = coap.get(self.server.url + "/test", confirmable=True, trace=True)
        self.assertEqual(r.sent.msgType, msgType.con)
        self.assertEqual(r.msgType, msgType.con)
        self.assertEqual(r.code, codes.content)
        self.assertNotIn(r.options, options.token)
        self.assertIn("Content-type", r)

        logging.info(r)

    #        self.assertEqual(Message.messageType.ACK, response.getType())
    #        self.assertEqual(new Option(TokenManager.emptyToken, options.TOKEN), response.getFirstOption(options.TOKEN))

    def test_TD_COAP_CORE_12(self):
        """
        Identifier: TD_COAP_CORE_12
        Objective: Handle request containing several URI-Path options
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            - Server offers a /seg1/seg2/seg3 resource

        Step 1 (stimulus) Client is requested to send a confirmable GET request to server’s resource

        Step 2 (Check (CON)) Sent request must contain:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - Option type = URI-Path (one for each path segment)

        Step 3 (Check (CON)) Server sends response containing:
            - Code = 69 (2.05 content)
            - Payload = Content of the requested resource
            - Content type option

        Step 4 (Verify (IOP)) Client displays the response
        """
        r = coap.get(self.server.url + "/seg1/seg2/seg3", trace=True, confirmable=True)
        self.assertEqual(r.sent.code, codes.GET)
        self.assertEqual(r.sent.msgType, msgType.con)
        self.assertIn(r.sent.options, ["seg1", "seg2", "seg3"])
        self.assertEqual(r.code, codes.content)
        self.assertEqual(r.payload, "TD_COAP_CORE_12")
        logging.info(r)

    def test_TD_COAP_CORE_13(self):
        """
        :Identifier: TD_COAP_CORE_13
        :Objective: Handle request containing several URI-Query options
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server offers a /query resource

        - Step 1: stimulus Client is requested to send a confirmable GET request with
            three Query parameters (e.g. ?first=1&second=2&third=3) to
            the server’s resource

        - Step 2: (Check (CON)) Sent request must contain:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - Option type = URI-Query (More than one query parameter)

        - Step 3: (Check (CON)) Server sends response containing:
            - Type = 0/2 (CON/ACK)
            - Code = 69 (2.05 content)
            - Payload = Content of the requested resource
            - Content type option

        - Step 4 (Verify (IOP)) Client displays the response
        """
        options = {"first": 1, "second": 2, "third": 3}
        r = coap.get(self.server.url + "/query", trace=True, confirmable=True,
            options=options)
        self.assertEqual(r.sent.msgType, msgType.con)
        self.assertEqual(r.sent.code, codes.GET)
        self.assertIn(r.sent.options[options.query], ["first", "second", "third"])
        self.assertEqual(r.code, codes.content)
        self.assertIn("Content-Type", r)
        self.assertTrue(r.msgType == msgType.con or r.msgType == msgType.ack)
        logging.info(r)

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
        r = coap.get(self.server.url + "/separate", confirmable=False)
        self.assertEqual(r.sent.code, codes.GET)
        self.assertEqual(r.sent.msgType, msgType.non)
        self.assertEqual(r.code, codes.content)
        self.assertEqual(r.msgType, msgType.non)
        self.assertIn("Content-Type", r)
        logging.info(r)

    def test_TD_COAP_CORE_17(self):
        """
        :Identifier: TD_COAP_CORE_17
        :Objective: Perform GET transaction with a separate response (NON mode)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Server offers a resource /separate which cannot be served immediately.

        - Step 1 (stimulus) Client is requested to send a non-confirmable GET request to server’s resource

        - Step 2 (check) The request sent by the client contains:
            - Type = 1 (NON)
            - Code = 1 (GET)
            - A message ID generated by the Client

        - Step 3 (check) Server DOES NOT send response containing:
            - Type = 2 (ACK)
            - Same message ID as in the request in step 2
            - empty Payload

        - Step 4 (check) Server sends response containing:
            - Type = 1 (NON)
            - Code = 69 (2.05 content)
            - Payload = Content of the requested resource
            - Content format option

        - Step 5 (verify) Client displays the response
        """
        r = coap.get(self.server.url + "/separate")
        self.assertEqual(r.sent.msgType, msgType.non)
        self.assertEqual(r.sent.code, codes.GET)
        self.assertNotEqual(r.msgType, msgType.ack)
        self.assertNotEqual(r.sent.messageID, r.messageID)
        self.assertNotEqual(r.payload, "")
        self.assertEqual(r.msgType, msgType.non)
        self.assertEqual(r.code, codes.content)
        logging.info(r)

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
        r = coap.post(self.server.url + "/test", payload="TD_COAP_CORE_18")
        self.assertEqual(r.sent.msgtype, msgType.con)
        self.assertEqual(r.sent.code, codes.post)
        self.assertEqual(r.code, codes.created)
        self.assertIn(["location1", "location2", "location3"], r.options)
        logging.info(r)

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
        r = coap.post(self.server.url + "/location-query",
            query={"first": 1, "second": 2},
            payload="TD_COAP_CORE_19")
        self.assertEqual(r.sent.msgtype, msgType.con)
        self.assertEqual(r.sent.code, codes.post)
        self.assertEqual(r.code, codes.created)
        self.assertEqual(r.options, {"first": 1, "second": 2})
        logging.info(r)

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

        - Step 2 (check) The request sent by the client contains:
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
        r = coap.get(self.server.url + "/multi-format", confirmable=True,
            options={"Accept": mediaCodes.text})
        self.assertEqual(r.sent.msgType, msgType.confirmable)
        self.assertEqual(r.sent.code, codes.GET)
        self.assertIn({"Accept": 1}, r.sent.options)
        self.assertEqual(r.code, codes.content)
        self.assertIn({"Content-Format": 1}, r.options)
        logging.info(r)
        opt = {options.accept: mediaCodes.xml}
        r = coap.get(self.server.url + "/multi-format", confirmable=True, options=opt)

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
        :Objective: Perform GET transaction with responses containing the
            ETag option and requests containing the If-Match option (CON mode)
        :Configuration: CoAP_CFG_01
        :Pre-test conditions:
            - Server should offer a /validate resource
            - Client & server supports ETag and If-Match option
            - The Client ‘s cache must be purged

        *Preamble* client gets the resource

        - Step 1 (stimulus) Client is requested to send a confirmable GET
            request to server’s resource

        - Step 2 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 1 (GET)

        - Step 3 (check) Server sends response containing:
            - Code = 69 (2.05 content)
            - Option type = ETag
            - Option value = an arbitrary Etag value
            - Not empty payload

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

        - Step 7 (verify) Client displays the response and the server changed
            its resource

        *Part B* concurrent updates

        - Step 8 (stimulus) Client is requested to send a confirmable GET request to
            server’s resource

        - Step 9 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 1 (GET)

        - Step 10 (check) The request sent by the client contains:
            - Code: 69 (2.05 content)
            - Option type: ETag
            - Option value = an arbitrary Etag value which differs from the ETag sent in step 3
            - The payload sent in step 5

        - Step 11 (verify) Client displays the response

        - Step 12 (stimulus) Update the content of the server’s resource from a CoAP client

        - Step 13 (stimulus) Client is requested to send a confirmable PUT
            request to server’s resource so as to perform an atomic update

        - Step 14 (check) The request sent by the client contains:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-Match
            - Option value=ETag value received in step 106
            - An arbitrary payload (which differs from the previous payloads)

        - Step 15 (check) Server sends response containing:
            - Code = 140 (4.12 Precondition Failed)

        - Step 16 (verify) Client displays the response and the server did
            not update the content of the resource
        """
        # Part A
        r = coap.get(self.server.url + "/test", confirmable=True)
        self.assertEqual(r.sent.msgType, msgType.con)
        self.assertEqual(r.sent.code, codes.put)

        # Part B

        r = coap.put(self.server.url + "/test")
        logging.info(r)


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

class TestLossy(unittest.TestCase):
    """
    Test suite for ETSI CoAP Core Tests (Lossy Context)


    - TD_COAP_CORE_15 Perform GET transaction (CON mode, piggybacked response)
        in a lossy context
    - TD_COAP_CORE_16 Perform GET transaction (CON mode, delayed response)
        in a lossy context
    """

    def setUp(self):
        """
        Implement a CoAP_CFG_02:
            Basic One-2-One CoAP client/server Configuration in lossy context

        The Gateway emulates a lossy medium between the client and the server.
        It does not implement the CoAP protocol itself (in other terms it is
        not a CoAP proxy), but works at the transport layer. It provides two
        features:
        - It performs NAT-style UDP port redirections towards the server
            (thus the client contacts the gateway and is transparently
            redirected towards the server)
        - It randomly drops packets that are forwarded between the client and
            the server
        """
        self.server = Endpoint(trace=True, lossy_factor=0.5)

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
        while self.server.drop_requests < 1\
        and self.server.drop_requests_ack < 1\
        and self.server.drop_response < 1\
        and self.server.drop_response_ack < 1:
            r = coap.get(self.server.url + "/test")
            self.assertEqual(r.sent.msgType, msgType.con)
            self.assertEqual(r.sent.code, codes.GET)
            self.assertIsNotNone(r.sent.messageID)


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


class TestProxy(unittest.TestCase):
    """
    Test suite for ETSI CoAP Core Tests Basic One-2-One CoAP proxy/server
    Configuration

    - TD_COAP_CORE_24 Perform POST transaction with responses containing
        several Location-Path options (Reverse Proxy in CON mode)
    - TD_COAP_CORE_24 Perform POST transaction with responses containing
        several Location- Query (Reverse proxy)
    - TD_COAP_CORE_24 Perform GET transaction containing the Accept option
        (CON mode) (Reverse proxy)
    - TD_COAP_CORE_24 Perform GET transaction with responses containing the
        ETag option and requests containing the If-Match option (CON mode)
        (Reverse proxy)
    - TD_COAP_CORE_24 Perform GET transaction with responses containing the
        ETag option and requests containing the If-None-Match option
        (CON mode) (Reverse proxy)
    - TD_COAP_CORE_24 Perform GET transaction with responses containing the
        Max-Age option (Reverse proxy)
    """

    def setUp(self):
        """
        Implement a CoAP_CFG_03:
        Basic One-2-One CoAP proxy/server Configuration

        The reverse proxy shown in the Figure 3 is assumed as CoAP/CoAP proxy.
        Test operator includes an interface (it can be a CoAP client) that
        creates the stimulus to initiate the tests for reverse proxy.

        More clearly, there exists two methods to create the stimulus for
        reverse proxy.
            1. Reverse proxy can provide a direct interface to create and
                launch the stimulus
            2. A CoAP client can be connected to reverse proxy to create and
                launch the stimulus for the tests
        In the both cases, reverse proxy and client equally act as point of
        observation.
        """
        self.proxy = Proxy("coap://localhost", port=5684, trace=True)  # Different port for the proxy
        self.server = Endpoint(trace=True)


    def test_TD_COAP_CORE_24(self):
        """
        :Identifier: TD_COAP_CORE_24
        :Objective: Perform POST transaction with responses containing
            several Location-Path options (Reverse Proxy in CON mode)

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
        payload = "TD_COAP_CORE_24"
        r = coap.post(self.proxy.url + "/test", confirmable=True)
        self.assertEqual(r.sent.msgType, msgType.con)
        self.assertEqual(r.sent.code, codes.post)
        self.assertEqual(r.sent.payload, payload)
        self.assertEqual(self.proxy.msg_sent[0].msgType, msgType.con)
        self.assertEqual(self.proxy.msg_sent[0].code, codes.post)
        self.assertEqual(self.proxy.msg_sent[0].payload, payload)
        self.assertEqual(self.proxy.msg_received[0].code, codes.created)

    def test_TD_COAP_CORE_25(self):
        """
        :Identifier: TD_COAP_CORE_25
        :Objective: Perform POST transaction with responses containing several Location- Query option (Reverse proxy)
        :Configuration: COAP_CFG_03

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
        r = coap.post(self.proxy.url + "/location-query", confirmable=True, query={"first": 1, "second": 2})
        logging.info(r)
        self.assertEqual(r.code, codes.created)
        self.assertEqual(r.url, self.proxy.url + "?first=1&second=2")

    def test_TD_COAP_CORE_26(self):
        """
        :Identifier: TD_COAP_CORE_26
        :Objective: Perform GET transaction containing the Accept option (CON mode)
        :Configuration: CoAP_CFG_03

        :Pre-test conditions:
            - Proxy is configured as a reverse-proxy for the server
            - Proxy’s cache is cleared
            - Server should provide a resource /multi-format which exists in
                two formats:
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
        # Part A
        r = coap.get(self.proxy.url + "/multi-format", confirmable=True)
        self.assertEqual(len(self.proxy.msg_received), 1)
        self.assertEqual(len(self.proxy.msg_sent), 1)
        self.assertEqual(self.proxy.msg_sent[0].msgType, msgType.con)
        self.assertEqual(self.proxy.msg_sent[0].code, codes.GET)
        self.assertEqual(self.proxy.msg_sent[0].options[options.accept], mediaCodes.text)
        self.assertEqual()
        # Part B
        r = coap.get(self.proxy.url + "/multi-format", confirmable=True)
        self.assertEqual(r.code, codes.content)
        self.assertEqual(r.msgType, codes.xml)
        # TODO

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

        - Step 13 (stimulus) Update the content of the server’s resource
            (either locally or from another CoAP client)

        - Step 14 (stimulus) Client is requested to send s confirmable PUT
            request to proxy so as to perform an atomic update

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
            - Option value=same ETag value found in step 14 An arbitrary
                payload (which differs from the previous payloads)

        - Step 18 (check) Server sends response containing:
            - Code = 140 (4.12 Precondition Failed)

        - Step 19 (Verify) Proxy forwards the response to client

        - Step 20 (check) Response contains:
            - Code = 140 (4.12 Precondition Failed)

        - Step 21 (Verify) Client displays the response

        """
        # Preamble
        r = coap.get(self.proxy.url, confirmable=True)
        self.assertEqual(self.proxy.msg_fowarded[0].url, self.server.url)
        self.assertEqual(self.proxy.msg_fowarded[0].msgType, msgType.con)
        self.assertEqual(self.proxy.msg_fowarded[0].code, codes.GET)
        self.assertEqual(self.server.msg_sent[0].code, codes.content)
        self.assertEqual(self.proxy.msg_fowarded[1].code, codes.content)
        self.assertIn(self.proxy.msg_fowarded[1].options, options.etag)

        # Part A

        # Part B
        self.assertEqual()
        self.assertEqual(r.code, codes.precondition_failed)
        logging.info(r)

    def test_TD_COAP_CORE_28(self):
        """
        :Identifier: TD_COAP_CORE_28
        :Objective: Perform GET transaction with responses containing the
            ETag option and requests containing the
            If-None-Match option (CON mode) (Reverse proxy)
        :Configuration: CoAP_CFG_03

        :Pre-test conditions:
            - Proxy is configured as a reverse-proxy for the server
            - Proxy’s cache is cleared
            - Server should offer a /test resource, which does not exist and
                which can be created by the client
            - Client & server supports If-None-Match

        *Part A*: single creation

        - Step 1 (stimulus) Client is requested to send a confirmable PUT
            request to proxy to atomically create resource in server

        - Step 2 (check) Proxy forwards the request to server

        - Step 3 (check) Forwarded request must contain:
            - Type = 0 (CON)
            - Code = 3 (PUT)
            - Option Type=If-None-Match
            - An arbitrary payload

        - Step 4 (check) Server sends response containing:
            - Code = 65 (2.01 Created)

        - Step 5 (check) Proxy forwards the response to client

        - Step 6 (verify) Client displays the response & and server created
            new resource

        *Part B*: concurrent creations

        - Step 5 (stimulus) Client is requested to send s confirmable PUT
            request to proxy to atomically create resource in server

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
        r = coap.put(self.proxy.url + "/test", confirmable=True)
        self.assertEqual(len(self.proxy.fowarded_msg), 1)
        self.assertEqual(self.proxy.fowarded_msg,)
        logging.info(r)


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

        - Step 6 (check) Proxy does not forward any request to the server

        - Step 7 (check) Proxy sends response to client

        - Step 8 (verify) Response contains:
            - Option type = Max-age
            - Option Value = new Max-age
            - Payload cached
        """
        max_age = 30  # seconds
        payload = "TD_COAP_CORE_29"
        r = coap.get(self.proxy.url + "/test", confirmable=True)
        self.assertEqual(self.proxy.msg_sent[0].msgType, msgType.con)
        self.assertEqual(self.proxy.msg_sent[0].code, codes.get)
        self.assertEqual(self.proxy.msg_received[0].code, codes.content)
        self.assertEqual(self.proxy.msg_received[0].options[options.etag], 42)  # TODO: Set this right
        self.assertEqual(self.proxy.msg_received[0].options[options.maxAge], max_age)
        r = coap.get(self.proxy.url + "/test", confirmable=True)
        self.assertEqual(len(self.proxy.msg_sent), 1)
        self.assertEqual(r.options[options.maxAge], max_age)
        self.assertEqual(r.payload, payload)

if __name__ == '__main__':
    unittest.main()
