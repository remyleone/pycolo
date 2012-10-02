# coding=utf-8

import unittest

from pycolo.coap import Request
from pycolo.coap import Response


class RequestTest(unittest.TestCase):

    class RespondTask():
        def __init__(self, request, response):
            super(self.RespondTask, self).__init__()
            self.request = request
            self.response = response

        def run(self):
            """ generated source for method run """
            self.request.respond(self.response)
            self.request.sendResponse()

        request = Request()
        response = Response()

    handledResponse = Response()

    def testRespond(self):
        """ generated source for method testRespond """
        #  Client Side ////////////////////////////////////////////////////////
        #  create new request with own response handler
        request = GETRequest()
        #  (...) send the request to server
        #  Server Side ////////////////////////////////////////////////////////
        #  (...) receive request from client
        #  create new response
        response = Response()
        #  respond to the request
        request.respond(response)
        request.sendResponse()
        #  Validation /////////////////////////////////////////////////////////
        #  check if response was handled correctly
        self.assertSame(response, self.handledResponse)

    def testReceiveResponse(self):
        """ generated source for method testReceiveResponse """
        #  Client Side ////////////////////////////////////////////////////////
        request = GETRequest()
        #  enable response queue in order to perform receiveResponse() calls
        request.enableResponseQueue(True)
        #  (...) send the request to server
        #  Server Side ////////////////////////////////////////////////////////
        #  (...) receive request from client
        #  create new response
        response = Response()
        #  schedule delayed response (e.g. take some time for computation etc.)
        self.timer.schedule(self.RespondTask(request, response), 500)
        #  Client Side ////////////////////////////////////////////////////////
        #  block until response received
        receivedResponse = request.receiveResponse()
        #  Validation /////////////////////////////////////////////////////////
        #  check if response was received correctly
        self.assertSame(response, receivedResponse)

    def testTokenManager(self):
        """ generated source for method testTokenManager """
        acquiredTokens = dict()
        emptyToken = [None] * 0
        acquiredTokens.add(emptyToken)
        print("Contains: " + acquiredTokens.contains(emptyToken))
        acquiredTokens.remove(emptyToken)
        print("Contains: " + acquiredTokens.contains(emptyToken))
