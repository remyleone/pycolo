# coding=utf-8

"""
TODO
"""

import unittest
from pycolo.endpoint import Endpoint
from pycolo.request import request as coap


class CarelessResource(Resource):
    """
    This class implements a 'separate' resource for demonstration purposes.
    Defines a resource that returns a response in a separate CoAP Message
    """
    def __init__(self,
                 title="This resource will ACK anything, but never send a separate response",
                 resourceType="SeparateResponseTester"):
        """
        :type title: title of the resource
        """
        self.title = title
        self.resourceType = resourceType

    def performGET(self, request):
        """
        promise the client that this request will be acted upon
        by sending an Acknowledgement...
        :param request:
        """
        request.accept()
        #  ... and then do nothing. Pretty mean.


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


class TestSimpleRequest(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        self.server = Endpoint()


    def test_piggyback(self):
        """

       Client  Server
          |      |
          |      |
          +----->|     Header: GET (T=CON, Code=1, MID=0x7d34)
          | GET  |   Uri-Path: "temperature"
          |      |
          |      |
          |<-----+     Header: 2.05 Content (T=ACK, Code=69, MID=0x7d34)
          | 2.05 |    Payload: "22.3 C"
          |      |


        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       | 1 | 0 |   1   |     GET=1     |          MID=0x7d34           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |  11   |  11   |      "temperature" (11 B) ...
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       | 1 | 2 |   0   |    2.05=69    |          MID=0x7d34           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |      "22.3 C" (6 B) ...
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

               Figure 16: Confirmable request; piggy-backed response

        :return:
        """
        sent_raw = b""
        received_raw = b""

        r = coap.get(self.server.url + "temperature", confirmable=True, messageID=0x7d34)
        self.assertEqual(r.sent.raw, sent_raw)
        self.assertEqual(r.raw, received_raw)

    def test_raw2(self):
        """
           Client  Server
              |      |
              |      |
              +----->|     Header: GET (T=CON, Code=1, MID=0x7d35)
              | GET  |      Token: 0x20
              |      |   Uri-Path: "temperature"
              |      |
              |      |
              |<-----+     Header: 2.05 Content (T=ACK, Code=69, MID=0x7d35)
              | 2.05 |      Token: 0x20
              |      |    Payload: "22.3 C"
              |      |


            0                   1                   2                   3
            0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           | 1 | 0 |   2   |     GET=1     |          MID=0x7d35           |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |   11   |  11   |      "temperature" (11 B) ...
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |   8    |   1   |     0x20      |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


            0                   1                   2                   3
            0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           | 1 | 2 |   1   |    2.05=69    |          MID=0x7d35           |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |Jump 15 = 0xf1 |  4    |   1   |     0x20      | "22.3 C" (6 B) ...
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

        :return:
        """
        sent_raw = b""
        received_raw = b""

        r = coap.get(self.server.url + "temperature", confirmable=True, messageID=0x7d34)
        self.assertEqual(r.sent.raw, sent_raw)
        self.assertEqual(r.raw, received_raw)


if __name__ == '__main__':
    unittest.main()
