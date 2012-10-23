# coding=utf-8

import datetime
import unittest

from threading import Timer

from pycolo.codes import codes, mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.resource import Resource


class Observe(Resource):
    """
    Observable resource which changes every 5 seconds.

    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.
    TD_COAP_OBS_01
    TD_COAP_OBS_02
    TD_COAP_OBS_03
    TD_COAP_OBS_04
    TD_COAP_OBS_05
    """
    #  The current time represented as string
    time = ""

    def __init__(self):
        self.title = "Observable resource which changes every 5 seconds"
        self.resourceType = "observe"
        self.observable = True
        Timer(5.0, self._update).start()  # Set timer task scheduling

    def _update(self):
        """ Defines a new timer task to return the current time """
        self.time = datetime.datetime.now().strftime("%H:%m:%S")
        self.changed()  # Call changed to notify subscribers

    def performGET(self, request):
        response = Response(codes.RESP_CONTENT)
        response.payload = self.time
        response.contentType = mediaCodes.text
        response.maxAge = 5
        request.respond(response)  # complete the request


class TestObserve(unittest.TestCase):

    def setUp(self):
        server = Endpoint()
        res = Observe()
        server.addResource(res)

    def test_observe(self):
        """
        Identifier: TD_COAP_OBS_01
        Objective: Handle resource observation
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports Observe option
            • Server supports Observe option
            • Server offers an observable resource /obs which changes periodically (e.g. every 5s)

        Step 1 stimulus Client is requested to observe resource /obs on Server

        Step 2 (check (CON)) Client sends a GET request containing Observe option
        indicating 0

        Step 3 (check (CON)) Server sends response containing Observe option

        Step 4 (verify (IOP)) Client displays the received information

        Step 5 (check (CON)) Server sends response containing Observe option indicating
        increasing values, as resource changes

        Step 6 (verify (IOP)) Client displays the updated information
        """
        pass

    def test_stop_observe(self):
        """
        :Identifier: TD_COAP_OBS_02
        :Objective: Stop resource observation
        :Configuration: CoAP_CFG_01

        Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every 5s)
            - Client is observing /obs on Server

        Step 1 stimulus Client is requested to stop observing resource /obs on Server

        Step 2 (check (CON))
        Client sends GET request not containing Observe option

        Step 3 (check (CON))
        Server sends response not containing Observe option

        Step 4 (verify (IOP)) Client displays the received information

        Step 5 (check (CON)) Server does not send further response

        Step 6 (verify (IOP)) Client does not display updated information
        """
        pass


    def test_detection_observe(self):
        """
        :Identifier: TD_COAP_OBS_03
        :Objective: Client detection of deregistration (Max-Age)
        :Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports Observe option
            • Server supports Observe option
            • Server offers an observable resource /obs which changes periodically (e.g. every
            5s)
            • Client is observing /obs on Server

        Step 1 stimulus Server is rebooted

        Step 2 (check (CON)) Server does not send notifications

        Step 3 (verify (IOP)) Client does not display updated information

        Step 4 (verify (IOP)) After Max-Age expiration, Client sends a new GET with
        Observe option for Server’s observable resource

        Step 5 (check (CON)) Sent request contains Observe option indicating 0

        Step 6 (check (CON)) Server sends response containing Observe option

        Step 7 (verify (IOP)) Client displays the received information

        Step 8 (check (CON)) Server sends response containing Observe option indicating
        increasing values, as resource changes

        Step 9 (verify (IOP)) Client displays the updated information
        """
        pass

    def test_detection_server(self):
        """
        Identifier: TD_COAP_OBS_04
        Objective: Server detection of deregistration (client OFF)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports Observe option
            • Server supports Observe option
            • Server offers an observable resource /obs which changes periodically (e.g. every 5s)
            • Client is observing /obs on Server

        Step 1 stimulus Client is switched off

        Step 2 (check (CON)) Server’s confirmable responses are not acknowledged

        Step 3 (verify (IOP)) After some delay, Server does not send further responses
        """
        pass

    def test_detection_RST(self):
        """
        Identifier: TD_COAP_OBS_05
        Objective: Server detection of deregistration (explicit RST)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports Observe option
            • Server supports Observe option
            • Server offers an observable resource /obs which changes periodically (e.g. every 5s)
            • Client is observing /obs on Server

        Step 1 stimulus Client is rebooted

        Step 2 (check (CON)) Server sends response containing Observe option

        Step 3 (verify (IOP)) Client discards response and does not display information

        Step 4 (check (CON)) Client sends RST to Server

        Step 5 (check (CON)) Server does not send further response
        """
        pass

if __name__ == '__main__':
    unittest.main()
