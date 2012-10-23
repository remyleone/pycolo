# coding=utf-8

import logging
import unittest
import sys
from pycolo import resource
from pycolo.Communicator import Communicator
from pycolo.message import Message
from pycolo.token import TokenManager
from pycolo.codes import options
from pycolo.request import request

class PlugtestClient(unittest.TestCase):

    PLUGTEST_BLOCK_SIZE = 64

    serverURI = "coap://localhost"

    # Use synchronous or asynchronous requests. Sync recommended due to single threaded servers and slow resources.
    sync = True

    def setUp(self):
        """
        Default constructor. Loads with reflection each nested class that is a
        derived type of self.
        @param serverURI the server uri
        :return:
        """

        # default block size
        Communicator.setupTransfer(codes.PLUGTEST_BLOCK_SIZE)

        if request.requiresToken():
            request.setToken(TokenManager.getInstance().acquireToken())


        request.registerResponseHandler(new TestResponseHandler())

        # enable response queue for synchronous I / O
        if sync:
            request.enableResponseQueue(True)

            # execute the request
            try {
                request.execute()
                if (sync) {
                    request.receiveResponse()
                }
            }

    def test_token(self):
        """
        Check token.
        @param expectedToken the expected token
        @param actualToken the actual token
        @return True, if successful
        """
        #
        success = True

        if expextedOption.equals(new Option(TokenManager.emptyToken, options.TOKEN)):
            self.assertEqual(None, actualOption)
        else:
            success = actualOption.getRawValue().length <= 8
            success &= actualOption.getRawValue().length >= 1

        # eval token length
        if not success:
            logging.info("FAIL: Expected token %s, but %s has illeagal length" % expextedOption, actualOption)
            
        success &= expextedOption.toString().equals(actualOption.toString())

    def test_checkDiscovery(expextedAttribute, actualDiscovery):
        """
        Check discovery.
        @param expextedAttribute the resource attribute to filter
        @param actualDiscovery the reported Link Format
        @return True, if successful
        :param actualDiscovery:
        :param expextedAttribute:
        """

        resource res = RemoteResource.newRoot(actualDiscovery)

        List < Option > query = new ArrayList < Option > ()
        query.add(new Option(expextedAttribute, options.URI_QUERY))

        success = True

        for sub in res.getSubResources():
            success &= LinkFormat.matches(sub, query)

            if not success:
                logging.info("FAIL: Expected %s, but was %s\n", expextedAttribute, LinkFormat.serialize(sub, null, false))

            if success:
                logging.info("PASS: Correct Link Format filtering")

    def test_CC01(self):
        """
        TD_COAP_CORE_01:
        Perform GET transaction (CON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 69

        r = request.get(self.serverURI + RESOURCE_URI)

        success &= checkType(Message.messageType["ACK"], r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)
        self.assertEqual(request.getMID(), r.MID)
        self.assertEqual(True, r.hasContentType())

        

    def test_CC02(self):
        """
        TD_COAP_CORE_02:
        Perform POST transaction (CON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 65

        payload = "TD_COAP_CORE_02"
        r = request.post(self.serverURI+ RESOURCE_URI, payload=payload)


        self.assertEqual(Message.messageType["ACK"], r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)
        self.assertEqual(request.getMID(), response.getMID(), "MID")

        

    def test_CC03(self):
        """
        TD_COAP_CORE_03:
        Perform PUT transaction (CON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 68

        r = request.put(self.serverURI + RESOURCE_URI, payload="TD_COAP_CORE_02")

        self.assertEqual(Message.messageType["ACK"], r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)

    def test_CC04(self):
        """
        TD_COAP_CORE_04:
        Perform DELETE transaction (CON mode).
        """
        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 66


        r = request.delete(serverURI + RESOURCE_URI)
        self.assertEqual(Message.messageType["ACK"], r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)


    def test_CC05(self):
        """
        TD_COAP_CORE_05:
        Perform GET transaction (NON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 69

        r = request.get(self.serverURI+ RESOURCE_URI, confirmable=False)

        self.assertEqual(Message.messageType["NON"], r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)
        self.assertEqual(True, r.hasContentType())


    def test_CC06(self):
        """
        TD_COAP_CORE_06:
        Perform POST transaction (NON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 65

        r = request.post(self.serverURI+ RESOURCE_URI,\
            confirmable=False,\
            payload="TD_COAP_CORE_06")

        self.assertEqual(Message.messageType["NON"], r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)

    def test_CC07(self):
        """
        TD_COAP_CORE_07:
        Perform PUT transaction (NON mode).
        """
        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 68

        # create the request
        r = request.put(self.serverURI+ RESOURCE_URI, confirmable=False, payload="TD_COAP_CORE_07")

        self.assertEqual(Message.messageType["NON"], r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")


    def test_CC08(self):
        """
        TD_COAP_CORE_08:
        Perform DELETE transaction (NON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 66

        r = request.delete(self.serverURI + RESOURCE_URI, confirmable=False)

        self.assertEqual(Message.messageType["NON"], r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, response.getCode(), "code")


    def test_CC09(self):
        """
        TD_COAP_CORE_09:
        Perform GET transaction with delayed response (CON mode, no piggyback).
        """

        RESOURCE_URI = "/separate"
        EXPECTED_RESPONSE_CODE = 69

        # create the request
        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True)


        self.assertEqual(Message.messageType["NON"], r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, response.code)
        self.assertEqual(True, r.hasContentType)

    def test_CC10(self):
        """
        TD_COAP_CORE_10:
        Handle request containing Token option.
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 69

        token = TokenManager.getInstance().acquireToken(False) # not preferring empty token
        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True, token=token)

        self.assertEqual(Message.messageType.ACK, r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")
        self.assertEqual(request.getFirstOption(options.TOKEN), response.getFirstOption(options.TOKEN))
        self.assertEqual(True, r.hasContentType)

    def test_CC11(self):
        """
        TD_COAP_CORE_11:
        Handle request not containing Token option.
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 69

        token = TokenManager.getInstance().acquireToken(True)
        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True, token=token)

        self.assertEqual(Message.messageType.ACK, response.getType())
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")
        self.assertEqual(new Option(TokenManager.emptyToken, options.TOKEN), response.getFirstOption(options.TOKEN))
        self.assertEqual(True, r.hasContentType())

        

    def test_CC12(self):
        """
        TD_COAP_CORE_12:
        Handle request containing several Uri - Path options.
        """

        RESOURCE_URI = "/seg1/seg2/seg3"
        EXPECTED_RESPONSE_CODE = 69

        Request request = request.get(self.serverURI + RESOURCE_URI, confirmable=True)
        executeRequest(request, serverURI, RESOURCE_URI)

        protected boolean checkResponse(Request request, Response response) {
            boolean success = True

        success &= checkType(Message.messageType.ACK, response.getType())
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")
        success &= hasContentType(response)

        

    def test_CC13(self):
        """
        TD_COAP_CORE_13:
        Handle request containing several Uri - Query options.
        """

        RESOURCE_URI = "/query"
        EXPECTED_RESPONSE_CODE = 69

        # create the request
        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True)
        # add query
        request.setOption(new Option("first=1", options.URI_QUERY))
        request.addOption(new Option("second=2", options.URI_QUERY))
        request.addOption(new Option("third=3", options.URI_QUERY))


        self.assertEqual(Message.messageType.ACK, response.getType()) || checkType(Message.messageType.CON, response.getType())
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")
        self.assertEqual(True, r.hasContentType(response))

        

    def test_CC16(self):
        """
        TD_COAP_CORE_16:
        Perform GET transaction with delayed response (NON mode).
        """

        RESOURCE_URI = "/separate"
        EXPECTED_RESPONSE_CODE = 69

        r =  request.get(self.serverURI + RESOURCE_URI, confirmable=False)

        self.assertEqual(Message.messageType.NON, r.type)
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)
        self.assertEqual(True, r.hasContentType())

    def test_CL01(self):
        """
        TD_COAP_LINK_01:
        Access to well - known interface for resource discovery.
        """

        RESOURCE_URI = "/.well-known/core"
        EXPECTED_RESPONSE_CODE = 69

        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True)

        self.assertEqual(Message.messageType.ACK, response.getType())
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")
        self.assertEqual(new Option(MediaTypeRegistry.APPLICATION_LINK_FORMAT, options.CONTENT_TYPE), response.getFirstOption(options.CONTENT_TYPE))

    def test_CL02(self):
        """
        TD_COAP_LINK_02:
        Use filtered requests for limiting discovery results.
        """

        RESOURCE_URI = "/.well-known/core"
        EXPECTED_RESPONSE_CODE = 69
        EXPECTED_RT = "rt=block"

        # create the request
        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True)
        # set query
        request.setOption(new Option(EXPECTED_RT, options.URI_QUERY))
        # set the parameters and execute the request

        self.assertEqual(Message.messageType.ACK, response.getType())
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")
        self.assertEqual(new Option(MediaTypeRegistry.APPLICATION_LINK_FORMAT, options.CONTENT_TYPE), response.getFirstOption(options.CONTENT_TYPE))
        self.assertEqual(EXPECTED_RT, response.getPayloadString())

        

    def test_CB01(self):
        """
        TD_COAP_BLOCK_01:
        Handle GET blockwise transfer for large resource (early negotiation).
        """

        RESOURCE_URI = "/large"
        EXPECTED_RESPONSE_CODE = 69

        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True)

        #request.setOption(new BlockOption(options.BLOCK2, 0, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false))


        self.assertEqual(True, r.hasOption(options.BLOCK2))

        # get actual number of blocks for check
        maxNUM = ((BlockOption)response.getFirstOption(options.BLOCK2)).getNUM()

        self.assertEqual(Message.messageType.ACK, response.getType())
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")
        self.assertEqual(
            new BlockOption(options.BLOCK2, maxNUM, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false),
                response.getFirstOption(options.BLOCK2))
        self.assertEqual(hasContentType(response)

    def test_CB02():
        """
        TD_COAP_BLOCK_02:
        Handle GET blockwise transfer for large resource (late negotiation).
        """

        RESOURCE_URI = "/large"
        EXPECTED_RESPONSE_CODE = 69

        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True)

        self.assertEqual(True, response.hasOption(options.BLOCK2))

        # get actual number of blocks for check
        maxNUM = ((BlockOption)response.getFirstOption(options.BLOCK2)).getNUM()

        self.assertEqual((Message.messageType.ACK, response.getType())
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)
        self.assertEqual(
            new BlockOption(options.BLOCK2, maxNUM, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false),
                response.getFirstOption(options.BLOCK2))
        self.assertEqual(True, r.hasContentType)

    def test_CB03(self):
        """
        TD_COAP_BLOCK_03:
        Handle PUT blockwise transfer for large resource.
        """

        RESOURCE_URI = "/large-update"
        EXPECTED_RESPONSE_CODE = 68

        payload = ""

        for i in range(20):
            for j in range(63):
                payload.append(int(i % 10))
                payload.append('\n')

        r = request.put(self.serverURI + RESOURCE_URI, confirmable=True, payload=payload)

        success = response.hasOption(options.BLOCK1)

        # get actual number of blocks for check
        maxNUM = ((BlockOption)response.getFirstOption(options.BLOCK1)).getNUM()

        self.assertEqual(Message.messageType.ACK, response.getType())
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")
        self.assertEqual(
            new BlockOption(options.BLOCK1, maxNUM, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false),
                response.getFirstOption(options.BLOCK1))


    def test_CB04(self):
        """
        TD_COAP_BLOCK_04:
        Handle POST blockwise transfer for large resource.
        """

        RESOURCE_URI = "/large-create"
        EXPECTED_RESPONSE_CODE = 65


        payload = ""

        for i in range(20):
            for j in range(63):
                payload.append(str(i % 10))
                payload.append('\n')

        r = request.post(self.server + RESOURCE_URI, confirmable=True, payload=payload)

        self.assertEqual(True, r.hasOption(options.BLOCK1))


        # get actual number of blocks for check
        maxNUM = ((BlockOption)response.getFirstOption(options.BLOCK1)).getNUM()

        self.assertEqual(Message.messageType.ACK, response.getType())
        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code, "code")
        self.assertEqual(
            new BlockOption(options.BLOCK1, maxNUM, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false),
                response.getFirstOption(options.BLOCK1))
        self.assertEqual(True, r.hasLocation)


    def test_CO01_02():
        """
        TD_COAP_OBS_01:
        Handle resource observation.
        TD_COAP_OBS_02:
        Stop resource observation.
        """

        RESOURCE_URI = "/obs"
        EXPECTED_RESPONSE_CODE = 69


        r = request.get(serverURI, RESOURCE_URI, confirmable=True)

        request.setOption(new Option(0, options.OBSERVE))

        self.assertEqual(codes.EXPECTED_RESPONSE_CODE, r.code)
        self.assertEqual(True, r.hasObserve(response))
        self.assertEqual(True, r.hasContentType(response))


        request.setURI(uri)
        if request.requiresToken():
            request.setToken(TokenManager.getInstance().acquireToken())

        # enable response queue for synchronous I / O
        request.enableResponseQueue(True)

        # for observing
        observeLoop = 5

        # print request info
        if verbose:
            logging.info("Request for test %s sent" % this.testName)
        request.prettyPrint()

        # execute the request
        try {
            Response response = null
            success = True

            request.execute()

            # receive multiple responses
            for i in range(l):
                response = request.receiveResponse()

                # checking the response
                if (response != null) {

                    # print response info
                    if self.verbose:
                        logging.info("Response received")
                        logging.info("Time elapsed (ms): %s" % response.getRTT())
                        response.prettyPrint()

                success &= checkResponse(response.getRequest(), response)

                if (! hasObserve(response)) {
                    break
                }
            }
        }

        # TD_COAP_OBS_02: Stop resource observation
        request.removeOptions(options.OBSERVE)
        request.setMID(-1)
        request.execute()
        response = request.receiveResponse()

        success &= hasObserve(response, True)

        if success:
            logging.info("**** TEST PASSED ****")
            addSummaryEntry("%s: PASSED" % testName)
        else:
            logging.info("**** TEST FAILED ****")
            addSummaryEntry("%s: FAILED" % testName)

    tickOffTest()

    } catch (IOException e) {
        logging.critical("Failed to execute request: %s" % e.getMessage())
        sys.exit(-1)
    } catch (InterruptedException e) {
        logging.critical("Interupted during receive: %s" % e.getMessage())
        sys.exit(-1)
    }

    def test_CO03_05(self):
        """
        TD_COAP_OBS_03:
        Client detection of deregistration (Max - Age).
        TD_COAP_OBS_05:
        Server detection of deregistration (explicit RST).
        """

        RESOURCE_URI = "/obs"
        EXPECTED_RESPONSE_CODE = 69

        private Timer timer = new Timer(True)


        # Utility class to provide transaction timeouts

        private class MaxAgeTask extends TimerTask {

            private Request request

        public MaxAgeTask(Request request) {
            this.request = request
        }

        @Override
        public void run() {
            this.request.handleTimeout()
        }
        }

        r = request.get(self.serverURI + RESOURCE_URI, confirmable=True)
        request.setOption(new Option(0, options.OBSERVE))
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = True

        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)
        self.assertEqual(True, r.hasObserve)
        self.assertEqual(True, r.hasContentType)

        protected synchronized void executeRequest(Request request, String serverURI, String resourceUri) {
        if (self.serverURI == null || serverURI.isEmpty()) {
            throw new IllegalArgumentException("serverURI == null || serverURI.isEmpty()")
        }

        # defensive check for slash
        if not serverURI.endsWith("/") and not resourceUri.startsWith("/")):
            resourceUri = "/" + resourceUri

        if request.requiresToken():
            request.setToken(TokenManager.getInstance().acquireToken())

    # enable response queue for synchronous I / O
    if sync:
        request.enableResponseQueue(True)

    # for observing
    int observeLoop = 5

    # print request info
    if self.verbose:
        logging.info("Request for test %s sent" % this.testName)
        request.prettyPrint()

    # execute the request
    try:

        success = True
        timedOut = False

        MaxAgeTask timeout = null

        request.execute()


    for (int l=0 l < observeLoop + +l) {

        response = request.receiveResponse()

        # checking the response
        if (response != null) {

            if (l >= 2 && ! timedOut) {
                logging.info("+++++++++++++++++++++++")
                logging.info("++++ REBOOT SERVER ++++")
                logging.info("+++++++++++++++++++++++")
            }

    if timeout:
        timeout.cancel()
        timer.purge()

    long time = response.getMaxAge() * 1000

    timeout = new MaxAgeTask(request)
    timer.schedule(timeout, time + 1000)

    # print response info
    if (verbose) {
        logging.info("Response received")
    logging.info("Time elapsed (ms): %s" % response.getRTT())
    response.prettyPrint()
    }

    success &= checkResponse(response.getRequest(), response)

    if (! hasObserve(response)) {
    break
    }

    } else {
        timedOut = True
    logging.info("PASS: Max-Age timed out")
    request.setMID(-1)
    request.execute()

    + +observeLoop
    }
    }


        }
    }


    def test_CO04(self):
        """
        TD_COAP_OBS_04:
        Server detection of deregistration (client OFF).
        """

        RESOURCE_URI = "/obs"
        EXPECTED_RESPONSE_CODE = 69

        # create the request
        r = request.get(self.serverURI + RESOURCE_URI)
        # set Observe option
        request.options[0] = options.OBSERVE


        self.assertEqual(EXPECTED_RESPONSE_CODE, r.code)
        self.assertEqual(True, r.hasObserve)
        self.assertEqual(True, r.hasContentType)

if __name__ == '__main__':
    unittest.main()
