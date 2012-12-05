# coding=utf-8

"""
Implementing ETSI Optional CoAP LINK Tests.
"""
import logging

import unittest
from pycolo.codes import mediaCodes, codes, msgType
from pycolo.endpoint import Endpoint

from pycolo.request import request


class LinkTest(unittest.TestCase):
    """
    This test suite will run all the ETSI test related to link format.

    - TD_COAP_LINK_01 Access to well-known interface for resource discovery
    - TD_COAP_LINK_02 Use filtered requests for limiting discovery results
    - TD_COAP_LINK_03 Handle empty prefix value strings
    - TD_COAP_LINK_04 Filter discovery results in presence of multiple rt
        attributes
    - TD_COAP_LINK_05 Filter discovery results using if attribute and prefix
        value strings
    - TD_COAP_LINK_06 Filter discovery results using sz attribute and prefix
        value strings
    - TD_COAP_LINK_07 Filter discovery results using href attribute and
        complete value strings
    - TD_COAP_LINK_08 Filter discovery results using href attribute and prefix
        value strings
    - TD_COAP_LINK_09 Arrange link descriptions hierarchically
    - TD_COAP_LINK_10 Handle an alternate link """

    def setUp(self):
        """
        Setting up a CoAP server running on localhost for testing.
        """
        server = Endpoint()
        server.discoveryResource()
        server.run()

    def test_TD_COAP_LINK_01(self):
        """
        :Identifier: TD_COAP_LINK_01
        :Objective: Access to well-known interface for resource discovery
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports CoRE Link Format
            - Server supports /.well-known/core resource and the CoRE Link
                Format

        - Step 1 (stimulus) Client is requested retrieve Server’s list of
            resource

        - Step 2 (check (CON)) Client sends a GET request to Server for
            /.well-known/core resource

        - Step 3 (check (CON)) Server sends response containing:
           - Content-Type option indicating 40 (application/link-format)
            payload indicating all the links available on Server

        - Step 4 (verify (IOP)) Client displays the list of resources available
            on Server
        """

        r = request.get(self.server.url + "/.well-known/core",
            confirmable=True)
        self.assertEqual(r.contentType, mediaCodes.link)
        self.assertEqual(r.code, codes.content)
        logging.info(r.payload)

    def test_TD_COAP_LINK_02(self):
        """
        :Identifier: TD_COAP_LINK_02
        :Objective: Use filtered requests for limiting discovery results
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports CoRE Link Format
            - Server supports CoRE Link Format
            - Server offers different types of resources (Type1, Type2, ...;
                see Note)

        - Step 1 (stimulus) Client is requested retrieve Server’s list of
            resource of a specific type Type1

        - Step 2 (check (CON)) Client sends a GET request to Server for
            /.well-known/core resource containing URI-Query indicating
            “rt=Type1”

        - Step 3 (check (CON)) Server sends response containing: Content-Type
            option indicating 40 (application/link-format) payload indicating
            only the links of type Type1 available on Server

        - Step 4 (verify (IOP)) Client displays the list of resources of type
            Type1 available on Server

        - Note: Type1, Type2, ... refer to real resource types available on
            Server and shall be extracted from Server’s /.well-known/core
            resource
        """
        r = request.get(self.server.url + "/.well-known/core",
            confirmable=True, query={"rt": "Type1"})
        self.assertEqual(r.contentType, mediaCodes.link)
        self.assertEqual(r.msgType, msgType.ack)
        self.assertEqual(r.code, codes.content)
        for i in r.payload:
            self.assertEqual(i["type"], "Type1")

    def test_TD_COAP_LINK_03(self):
        """
        :Identifier: TD_COAP_LINK_03
        :Objective: Handle empty prefix value strings
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Core Link Format
            - Server supports Core Link Format
            - Server offers different types of resources (Type1, Type2, ...;
                see Note)
            - Server offers resources with no type (i.e. no rt attribute)

        - Step 1 (stimulus) Client is requested to retrieve Server’s list of
            resources matching an rt empty value

        - Step 2 (check) Client sends a GET request to Server for
            /.well-known/core resource containing URI-Query indicating rt=“”

        - Step 3 (check) Server sends response containing:
            - Content-format option indicating 40 (application/link-format)
            - Payload indicating only the links having an rt attribute

        - Step 4 (verify) Client displays the list of resources with rt
            attribute available on Server

        Note: Type1, Type2, ... refer to real resource types available on
            Server and shall be extracted from Server’s /.well-known/core
            resource
        """
        r = request.get(self.server.url + "/.well-known/core",
            query={"rt": ""})
        self.assertEqual(r.contentType, mediaCodes.link)
        for i in r.payload:
            self.assertIn(i, "rt")

    def test_TD_COAP_LINK_04(self):
        """
        :Identifier: TD_COAP_LINK_04
        :Objective: Filter discovery results in presence of multiple rt
            attributes
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Core Link Format
            - Server supports Core Link Format
            - Server offers 4 groups of resources:
                1. Resources with rt=“Type1 Type2”
                2. Resources with rt=“Type2 Type3”
                3. Resources with rt=“Type1 Type3”
                4. Resources with rt=“”

        - Step 1 (stimulus) Client is requested to retrieve Server’s list of
            resources of a specific type Type2

        - Step 2 (check) Client sends a GET request to Server for
            /.well-known/core resource containing URI-Query indicating
            rt=“Type2”

        - Step 3 (check) Server sends response containing:
            - Content-format option indicating 40 (application/link-format)
            - Payload indicating only the links of groups 1 and 2
        """
        r = request.get(self.server.url + "/.well-known/core",
            query={"rt": "Type2"})
        self.assertEqual(r.contentType, mediaCodes.link)
        for i in r.payload:
            self.assertIn("Type2", i["rt"])

    def test_TD_COAP_LINK_05(self):
        """
        :Identifier: TD_COAP_LINK_05
        :Objectives: Filter discovery results using if attribute and prefix
            value strings
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Core Link Format
            - Server supports Core Link Format
            - Server offers 4 groups of resources:
                1. Resources with if=“If1”
                2. Resources with if=“If2”
                3. Resources with if=“foo”
                4. Resources with no if attribute

        - Step 1 (stimulus) Client is requested to retrieve Server’s list of
            resources matching the interface description pattern “If*”

        - Step 2 (check) Client sends a GET request to Server for
            /.well-known/core resources containing URI-Query indicating
            if=“If*”

        - Step 3 (check) Server sends response containing:
            - Content-format option indicating 40 (application/link-format)
            - Payload indicating only the links of groups 1 and 2

        - Step 4 (verify) Client displays the retrieved list of resources
        """
        r = request.get(self.server.url + "/.well-known/core",
            query={"if": "If*"})
        self.assertEqual(r.contentType, mediaCodes.link)
        for i in r.payload:
            self.assertTrue(i["if"].startwith("If"))
        logging.info(r.payload)

    def test_TD_COAP_LINK_06(self):
        """
        :Identifier: TD_COAP_LINK_06
        :Objective: Filter discovery results using sz attribute and prefix
            value strings
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Core Link Format
            - Server supports Core Link Format
            - Server offers resource with sz attribute
            - Server offers resources with no sz attribute

        - Step 1 (stimulus) Client is requested to retrieve Server’s list of
            resources having a sz attribute

        - Step 2 (check) Client sends a GET request to Server for
            /.well-known/core resource containing URI-Query indicating sz=“*”

        - Step 3 (check) Server sends response containing:
            - Content-format option indicating 40 (application/link-format)
            - Payload indicating only the links having a sz attribute

        - Step 4 (verify) Client displays the retrieved list of resources
        """
        r = request.get(self.server.url + "/.well-known/core",
            query={"sz": "*"})
        self.assertEqual(r.contentType, mediaCodes.link)
        for i in r.payload:
            self.assertIn("sz", i)
        logging.info(r.payload)

    def test_TD_COAP_LINK_07(self):
        """
        :Identifier: TD_COAP_LINK_07
        :Objective: Filter discovery results using href attribute and
            complete value strings
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Core Link Format
            - Server supports Core Link Format
            - Server offers resources /link1 /link2 and /link3

        - Step 1 (stimulus) Client is requested to retrieve the link-value
            anchored at /link1

        - Step 2 (check) Client sends a GET request to Server for
            /.well-known/core resource containing URI-Query indicating
            href=“/link1”

        - Step 3 (check) Server sends response containing:
            Content-format option indicating 40 (application/link-format)
            Payload indicating only the link for /link1

        - Step 4 (verify) Client displays the retrieved list of resources
        """
        r1 = request.get(self.server.url + "/.well-known/core",
            query={"href": "/link1"})
        self.assertEqual(r1.contentType, mediaCodes.link)
        r2 = request.get(self.server.url + "/link1")
        self.assertIn(r1.payload, r2.payload)
        logging.info(r1.payload)

    def test_TD_COAP_LINK_08(self):
        """
        :Identifier: TD_COAP_LINK_08
        :Objective: Filter discovery results using href attribute and prefix
            value strings
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Core Link Format
            - Server supports Core Link Format
            - Server offers resources /link1 /link2 and /link3
            - Server offers resource /test

        - Step 1 (stimulus) Client is requested to retrieve the link-value
            anchored at /link*

        - Step 2 (check) Client sends a GET request to Server for
            /.well-known/core resource containing URI-Query indicating
            href=“/link*”

        - Step 3 (check) Server sends response containing:
            - Content-format option indicating 40 (application/link-format)
            - Payload indicating only the link matching /link*

        - Step 4 (verify) Client displays the retrieved list of resources
        """
        r = request.get(self.server.url + "/.well-known/core",
            query={"href": "/link*"})
        self.assertEqual(r.contentType, mediaCodes.link)
        for i in r.payload:
            self.assertTrue(i.startwith("/link"))
        logging.info(r.payload)

    def test_TD_COAP_LINK_09(self):
        """
        :Identifier: TD_COAP_LINK_09
        :Objective: Arrange link descriptions hierarchically
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Core Link Format
            - Server supports Core Link Format
            - Server offers an entry located at /path with ct=40
            - Server offers sub-resources /path/sub1, /path/sub2, ... (see
                Note)

        - Step 1 (stimulus) Client is requested to retrieve one of the
            sub-resources

        - Step 2 (check) Client sends a GET request to Server for
            /.well-known/core resource

        - Step 3 (check) Server sends response containing:
            - Content-format option indicating 40 (application/link-format)
            - Payload indicating the link description for /path

        - Step 4 (check) Client sends a GET request for /path to Server

        - Step 5 (check) Server sends response containing:
            - Content-format option indicating 40 (application/link-format)
            - Payload indicating the link description for /path/sub1,
                /path/sub2, ...

        - Step 6 (check) Client sends a GET request for /path/sub1

        - Step 7 (check) Server sends 2.05 (Content) response. Payload contains
            /path/sub1

        - Step 8 (verify) Client displays the retrieved sub-resource.

        Note: /path/sub1, /path/sub2, ... refer to real resources available on
            Server and shall be extracted from Server’s /.well-known/core
            resource
        """
        r = request.get(self.server.url + "/.well-known/core")
        self.assertEqual(r.contentType, mediaCodes.link)
        r = request.get(self.server.url + r.payload)
        self.assertEqual(r.contentType, mediaCodes.link)
        self.assertIn(["/path/sub1", "/path/sub2"], r.payload)
        for sub_resource in r.payload:
            sub = request.get(self.server.url + sub_resource)
            logging.info(sub.payload)

    def test_TD_COAP_LINK_10(self):
        """
        :Identifier: TD_COAP_LINK_10
        :Objective: Handle an alternate link
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Core Link Format
            - Server supports Core Link Format
            - Server offers resources /test and /alternate (see Note)
            - Resource /alternate is anchored at /test (i.e. anchor=”/test”)
                with rel=”alternate”

        - Step 1 (stimulus) Client is requested to retrieve the resource /test
            using the alternate /alternate

        - Step 2 (check) Client sends a GET request to Server for /alternate

        - Step 3 (check) Server sends response containing the resource /test

        - Step 4 (verify) Client displays the response

        Note: /test and /alternate refer to a real resource and its alternate
            available on Server and shall be extracted from Server’s
            /.well-known/core resource
        """
        r1 = request.get(self.server.url + "/alternate")
        r2 = request.get(self.server.url + "/test")
        self.assertEqual(r1.payload, r2.payload)

if __name__ == '__main__':
    unittest.main()
