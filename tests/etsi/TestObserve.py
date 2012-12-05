# coding=utf-8

"""
Testing observation as specified in the ETSI IoT CoAP Plugtests.
"""

import datetime
import logging
import unittest

from threading import Timer

from pycolo.codes import codes, mediaCodes, options, msgType
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.request import request as coap
from pycolo.resource import Resource
from tests.etsi import Observe


class TestObserve(unittest.TestCase):
    """
    Test suite for ETSI Optional CoAP OBSERVE Tests

    - TD_COAP_OBS_01 Handle resource observation with CON messages
    - TD_COAP_OBS_02 Handle resource observation with NON messages
    - TD_COAP_OBS_03 Stop resource observation
    - TD_COAP_OBS_04 Client detection of deregistration (Max-Age)
    - TD_COAP_OBS_05 Server detection of deregistration (client OFF)
    - TD_COAP_OBS_06 Server detection of deregistration (explicit RST)
    - TD_COAP_OBS_07 Server cleans the observers list on DELETE
    - TD_COAP_OBS_08 Server cleans the observers list when observed resource content-format changes
    - TD_COAP_OBS_09 Update of the observed resource
    """

    def setUp(self):
        """
        Set up a configuration as specified in CoAP_CFG_01
        """
        server = Endpoint()
        res = Observe()
        server.addResource(res)

    def callback_TD_COAP_OBS_01(self, r):
        """
        TODO

        :param r:
        :return:
        """
        logging.info(r)

    def test_TD_COAP_OBS_01(self):
        """
        :Identifier: TD_COAP_OBS_01
        :Objective: Handle resource observation
        :Configuration: CoAP_CFG_01

        - Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes
                periodically (e.g. every 5s)  which produces confirmable
                notifications

        - Step 1 stimulus Client is requested to observe resource /obs on
            Server

        - Step 2 (check (CON)) Client sends a GET request containing Observe
            option indicating 0

        - Step 3 (check (CON)) Server sends response containing Observe option

        - Step 4 (verify (IOP)) Client displays the received information

        - Step 5 (check (CON)) Server sends response containing Observe option
            indicating increasing values, as resource changes

        - Step 6 (verify (IOP)) Client displays the updated information
        """
        r = coap.observe(self.server.url + "/obs",
            callback=self.callback_TD_COAP_OBS_01)
        self.assertin(r.options, options.observe)

    def test_TD_COAP_OBS_02(self):
        """
        :Identifier: TD_COAP_OBS_02
        :Objective: Stop resource observation
        :Configuration: CoAP_CFG_01

        - Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs-non which changes
                periodically (e.g. every 5s) which produces non-confirmable
                notifications
            - Client is observing /obs on Server

        - Step 1 stimulus Client is requested to stop observing resource /obs on Server

        - Step 2 (check (CON))
            Client sends GET request not containing Observe option

        - Step 3 (check (CON))
            Server sends response not containing Observe option

        - Step 4 (verify (IOP)) Client displays the received information

        - Step 5 (check (CON)) Server does not send further response

        - Step 6 (verify (IOP)) Client does not display updated information
        """
        r = coap.get(self.server.url + "/obs", observable=True)
        r = coap.get(self.server.url + "/obs")
        self.assertNotIn(options.observe, r.options)
        logging.info(r)


    def test_TD_COAP_OBS_03(self):
        """
        :Identifier: TD_COAP_OBS_03
        :Objective: Client detection of deregistration (Max-Age)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every
              5s) which produces confirmable notifications
            - Client is observing /obs on Server

        - Step 1 stimulus Server is rebooted

        - Step 2 (check (CON)) Server does not send notifications

        - Step 3 (verify (IOP)) Client does not display updated information

        - Step 4 (verify (IOP)) After Max-Age expiration, Client sends a new GET with
            Observe option for Server’s observable resource

        - Step 5 (check (CON)) Sent request contains Observe option indicating 0

        - Step 6 (check (CON)) Server sends response containing Observe option

        - Step 7 (verify (IOP)) Client displays the received information

        - Step 8 (check (CON)) Server sends response containing Observe option indicating
            increasing values, as resource changes

        - Step 9 (verify (IOP)) Client displays the updated information
        """
        pass

    def test_TD_COAP_OBS_04(self):
        """
        :Identifier: TD_COAP_OBS_04
        :Objective: Server detection of deregistration (client OFF)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes
                periodically (e.g. every 5s) which produces confirmable
                notifications
            - Client is observing /obs on Server

        - Step 1 stimulus Client is switched off

        - Step 2 (check (CON)) Server’s confirmable responses are not
            acknowledged

        - Step 3 (verify (IOP)) After some delay, Server does not send further
            responses
        """
        r = coap.observe(self.server.url + "/obs")

        #        RESOURCE_URI = "/obs"
        #        EXPECTED_RESPONSE_CODE = 69
        #
        #        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)
        #        self.assertEqual(True, r.hasObserve)
        #        self.assertEqual(True, r.hasContentType)


    def test_TD_COAP_OBS_05(self):
        """
        :Identifier: TD_COAP_OBS_05
        :Objective: Server detection of deregistration (explicit OFF)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes
                periodically (e.g. every 5s) which produces confirmable
                notifications
            - Client is observing /obs on Server

        - Step 1 stimulus Client is rebooted

        - Step 2 (check (CON)) Server sends response containing Observe option

        - Step 3 (verify (IOP)) Client discards response and does not display
            information

        - Step 4 (check (CON)) Client sends RST to Server

        - Step 5 (check (CON)) Server does not send further response
        """
        pass

    def test_TD_COAP_OBS_06(self):
        """
        :Identifier: TD_COAP_OBS_06
        :Objective: Server detection of deregistration (explicit RST)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes
                periodically (e.g. every 5s) which produces confirmable
                notifications

        - Step 1 Stimulus Client is requested to send to the server a GET
            request with observe option for resource /obs

        - Step 2 (check): The request sent by client contains:
            - Type = 1 (CON)
            - Code = 1 (GET)
            - Token value = a value generated by the client
            - Observe option = empty

        - Step 3 (check): Server sends a notification containing:
            - Type = 1 (CON)
            - Content-format = the same for all notifications
            - Token value = same as one found in the step 2
            - Observe option indicating increasing values

        - Step 4 (check): Client displays the received information

        - Step 5 (check): Client sends an ACK

        - Step 6 (Stimulus): Client is rebooted

        - Step 7 (check): Server is still sending notifications for the
            request in step 2. Notification contains:
            - Type = 1 (CON)
            - Content-format = the same for all notifications
            - Token value = same as one found in the step 2
            - Observe option indicating increasing values

        - Step 8 (verify): Client discards response and does not display information

        - Step 9 (check): Client sends RST to Server

        - Step 10 (verify): Server does not send further response

        Notes:
            (1) Steps 3-5 are in a loop.
            (2) Step 6-10 are asynchronous to the loop.
        """
        pass

    def test_TD_COAP_OBS_07(self):
        """
        :Identifier: TD_COAP_OBS_07
        :Objective: Server cleans the observers list on DELETE
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes
                periodically (e.g. every 5s) which produces confirmable
                notifications

        - Step 1 (stimulus): Client is requested to send to the server a GET
            request with observe option for resource /obs

        - Step 2 (check): The request sent by client contains:
            - Type = 1 (CON)
            - Code = 1 (GET)
            - Token value = a value generated by the client
            - Observe option = empty

        - Step 3 (check): Server sends a notification containing:
            - Type = 1 (CON)
            - Content-format = the same for all notifications
            - Token value = same as one found in the step 2
            - Observe option indicating increasing values

        - Step 4 (check): Client displays the received information

        - Step 5 (check): Client sends an ACK

        - Step 6 (stimulus): Client is requested to send to the server a
            DELETE request with observe option for resource /obs

        - Step 7 (check): The request sent by client contains:
            - Type = 1(NON)
            - Code = 4(DELETE)

        - Step 8 (check): Server sends response containing:
            - Type = 1(CON)
            - Code = 66(2.02 Deleted)

        - Step 9 (check): Server sends 4.04 (Not Found) response to the
            observer registered for /obs

        - Step 10 (verify): Server does not send further responses

        Notes:
            (1) Steps 3-5 are in a loop.
            (2) Step 6-10 are asynchronous to the loop.
            (3) Steps 8 and 9 may occur out-of-order
        """
        r = coap.observe(self.server.url + "/obs")
        self.assertEqual(r.msgType, msgType.con)
        self.assertEqual(r.code, codes.GET)

    def test_TD_COAP_OBS_08(self):
        """
        :Identifier: TD_COAP_OBS_08
        :Objective: Server cleans the observers list when observed resource
            content-format changes
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes
                periodically (e.g. every 5s) which produces confirmable
                notifications

        - Step 1 (stimulus): Client is requested to send to the server a GET
            request with observe option for resource /obs

        - Step 2 (check): The request sent by client contains:
            - Type = 1 (CON)
            - Code = 1 (GET)
            - Token value  = a value generated by the client
            - Observe option = None

        - Step 3 (check): Server sends a notification containing:
            - Type = 1 (CON)
            - Content-format = the same for all notifications
            - Token value = same as one found in the step 2
            - Observe option indicating increasing values

        - Step 4 (check): Client displays the received information

        - Step 5 (check): Client sends an ACK

        - Step 6 (stimulus): Client is requested to update the /obs content-
            format on Server

        - Step 7 (check): Client sends a POST request for /obs indicating a
            different content-format from one received in step 3

        - Step 8 (check): Server sends 2.04 (Changed) to the client

        - Step 9 (check): Server sends 5.00 (Internal Server Error) to the
            observer registered for /obs

        - Step 10 (Verify): Server does not send further notifications

        Notes:
            (1) Steps 3-5 are in a loop.
            (2) Step 6-10 are asynchronous to the loop.
            (3) Steps 8 and 9 may occur out-of-order
        """
        pass

    def callback_TD_COAP_OBS_09(self, r):
        self.assertEqual(r.msgType, msgType.ack)
        self.assertEqual()


    def test_TD_COAP_OBS_09(self):
        """
        :Identifier: TD_COAP_OBS_09
        :Objective: Update of the observed resource
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes
                periodically (e.g. every 5s) which produces confirmable
                notifications

        - Step 1 (stimulus) Client is requested to send to the server a
            confirmable GET request with observe option for resource /obs

        - Step 2 (check) The request sent by clients contains:
            - Type = 0 (CON)
            - Code = 1 (GET)
            - Token value = a value generated by the client
            - Observe option = empty

        - Step 3 (check) Server sends the response containing:
            - Type = 2 (ACK)
            - Content-format of the resource /obs
            - Token value = same as one found in the step 2
            - Observe option with a sequence number
        """
        r = coap.observe(self.server.url + "/obs",
            callback=self.callback_TD_COAP_OBS_09,
            confirmable=True)
        self.assertEqual(r.sent.msgType, msgType.con)
        self.assertEqual(r.sent.code, codes.GET)
        self.assertEqual(r.sent.options)

if __name__ == '__main__':
    unittest.main()



    def test_CO03_05(self):
        """
        TD_COAP_OBS_03:
        Client detection of de registration (Max - Age).
        TD_COAP_OBS_05:
        Server detection of de registration (explicit RST).
        """

        #        RESOURCE_URI = "/obs"
        #        EXPECTED_RESPONSE_CODE = 69
        #
        #        private Timer timer = new Timer(True)
        #
        #
        #        # Utility class to provide transaction timeouts
        #
        #        private class MaxAgeTask extends TimerTask {
        #
        #            private Request request
        #
        #        public MaxAgeTask(Request request) {
        #            this.request = request
        #        }
        #
        #        @Override
        #        public void run() {
        #            this.request.handleTimeout()
        #        }
        #        }
        #
        #        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True)
        #        request.setOption(new Option(0, options.OBSERVE))
        #        }
        #
        #        protected boolean checkResponse(Request request, Response response) {
        #            boolean success = True
        #
        #        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)
        #        self.assertEqual(True, r.hasObserve)
        #        self.assertEqual(True, r.hasContentType)
        #
        #        protected synchronized void executeRequest(Request request, String serverURI, String resourceUri) {
        #        if (self.serverURI == null || serverURI.isEmpty()) {
        #            throw new IllegalArgumentException("serverURI == null || serverURI.isEmpty()")
        #        }
        #
        #        # defensive check for slash
        #        if not serverURI.endsWith("/") and not resourceUri.startsWith("/")):
        #            resourceUri = "/" + resourceUri
        #
        #        if request.requiresToken():
        #            request.setToken(TokenManager.getInstance().acquireToken())
        #
        #    # enable response queue for synchronous I / O
        #    if sync:
        #        request.enableResponseQueue(True)
        #
        #    # for observing
        #    int observeLoop = 5
        #
        #    # print request info
        #    if self.verbose:
        #        logging.info("Request for test %s sent" % this.testName)
        #        request.prettyPrint()
        #
        #    # execute the request
        #    try:
        #
        #        success = True
        #        timedOut = False
        #
        #        MaxAgeTask timeout = null
        #
        #        request.execute()
        #
        #
        #    for (int l=0 l < observeLoop + +l) {
        #
        #        response = request.receiveResponse()
        #
        #        # checking the response
        #        if (response != null) {
        #
        #            if (l >= 2 && ! timedOut) {
        #                logging.info("+++++++++++++++++++++++")
        #                logging.info("++++ REBOOT SERVER ++++")
        #                logging.info("+++++++++++++++++++++++")
        #            }
        #
        #    if timeout:
        #        timeout.cancel()
        #        timer.purge()
        #
        #    long time = response.getMaxAge() * 1000
        #
        #    timeout = new MaxAgeTask(request)
        #    timer.schedule(timeout, time + 1000)
        #
        #    # print response info
        #    if (verbose) {
        #        logging.info("Response received")
        #    logging.info("Time elapsed (ms): %s" % response.getRTT())
        #    response.prettyPrint()
        #    }
        #
        #    success &= checkResponse(response.getRequest(), response)
        #
        #    if (! hasObserve(response)) {
        #    break
        #    }
        #
        #    } else {
        #        timedOut = True
        #    logging.info("PASS: Max-Age timed out")
        #    request.setMID(-1)
        #    request.execute()
        #
        #    + +observeLoop
        #    }
        #    }
        #
        #
        #        }
        #    }



    def test_CO01_02(self):
        """
        TD_COAP_OBS_01:
        Handle resource observation.
        TD_COAP_OBS_02:
        Stop resource observation.
        """

        #        RESOURCE_URI = "/obs"
        #        EXPECTED_RESPONSE_CODE = 69
        #
        #
        #        r = request.get(serverURI, RESOURCE_URI, confirmable=True)
        #
        #        request.setOption(new Option(0, options.OBSERVE))
        #
        #        self.assertEqual(codes.EXPECTED_RESPONSE_CODE, r.code)
        #        self.assertEqual(True, r.hasObserve(response))
        #        self.assertEqual(True, r.hasContentType(response))
        #
        #
        #        request.setURI(uri)
        #        if request.requiresToken():
        #            request.setToken(TokenManager.getInstance().acquireToken())
        #
        #        # enable response queue for synchronous I / O
        #        request.enableResponseQueue(True)
        #
        #        # for observing
        #        observeLoop = 5
        #
        #        # print request info
        #        if verbose:
        #            logging.info("Request for test %s sent" % this.testName)
        #        request.prettyPrint()
        #
        #        # execute the request
        #        try {
        #            Response response = null
        #            success = True
        #
        #            request.execute()
        #
        #            # receive multiple responses
        #            for i in range(l):
        #                response = request.receiveResponse()
        #
        #                # checking the response
        #                if (response != null) {
        #
        #                    # print response info
        #                    if self.verbose:
        #                        logging.info("Response received")
        #                        logging.info("Time elapsed (ms): %s" % response.getRTT())
        #                        response.prettyPrint()
        #
        #                success &= checkResponse(response.getRequest(), response)
        #
        #                if (! hasObserve(response)) {
        #                    break
        #                }
        #            }
        #        }
        #
        #        # TD_COAP_OBS_02: Stop resource observation
        #        request.removeOptions(options.OBSERVE)
        #        request.setMID(-1)
        #        request.execute()
        #        response = request.receiveResponse()
        #
        #        success &= hasObserve(response, True)
        #
        #    tickOffTest()
        #
        #    } catch (IOException e) {
        #        logging.critical("Failed to execute request: %s" % e.getMessage())
        #        sys.exit(-1)
        #    } catch (InterruptedException e) {
        #        logging.critical("Interupted during receive: %s" % e.getMessage())
        #        sys.exit(-1)
        #    }
