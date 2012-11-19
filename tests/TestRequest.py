# coding=utf-8

"""
TODO
"""

import unittest


class RequestTest(unittest.TestCase):
    """
    TODO
    """
    class RespondTask():
        """
        TODO
        """
        pass
    #        def __init__(self, request, response):
    #            super(self.RespondTask, self).__init__()
    #            self.request = request
    #            self.response = response
    #
    #        def run(self):
    #            """ generated source for method run """
    #            self.request.respond(self.response)
    #            self.request.sendResponse()
    #
    #        request = request()
    #        response = Response()
    #
    #    handledResponse = Response()

    def testRespond(self):
        """
        TODO
        """
        pass

    #        #  Client Side ////////////////////////////////////////////////////////
    #        #  create new request with own response handler
    #        request = GETRequest()
    #        #  (...) send the request to server
    #        #  Server Side ////////////////////////////////////////////////////////
    #        #  (...) receive request from client
    #        #  create new response
    #        response = Response()
    #        #  respond to the request
    #        request.respond(response)
    #        request.sendResponse()
    #        #  Validation /////////////////////////////////////////////////////////
    #        #  check if response was handled correctly
    #        self.assertSame(response, self.handledResponse)

    def testReceiveResponse(self):
        """
        TODO
        """
        pass

    #        #  Client Side ////////////////////////////////////////////////////////
    #        request = GETRequest()
    #        #  enable response queue in order to perform receiveResponse() calls
    #        request.enableResponseQueue(True)
    #        #  (...) send the request to server
    #        #  Server Side ////////////////////////////////////////////////////////
    #        #  (...) receive request from client
    #        #  create new response
    #        response = Response()
    #        #  schedule delayed response (e.g. take some time for computation etc.)
    #        self.timer.schedule(self.RespondTask(request, response), 500)
    #        #  Client Side ////////////////////////////////////////////////////////
    #        #  block until response received
    #        receivedResponse = request.receiveResponse()
    #        #  Validation /////////////////////////////////////////////////////////
    #        #  check if response was received correctly
    #        self.assertSame(response, receivedResponse)

    def testTokenManager(self):
        """
        TODO
        """
        pass

    #        acquiredTokens = {}
#        emptyToken = [None] * 0
#        acquiredTokens.add(emptyToken)
#        print("Contains: %s" % acquiredTokens.contains(emptyToken))
#        acquiredTokens.remove(emptyToken)
#        print("Contains: %s" % acquiredTokens.contains(emptyToken))


class TestSeparate(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        # sep = Separate()
        pass




if __name__ == '__main__':
    unittest.main()
