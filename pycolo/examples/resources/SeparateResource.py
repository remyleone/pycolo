# coding=utf-8

from pycolo.coap import CodeRegistry
from pycolo.coap import GETRequest
from pycolo.coap import Response
from pycolo.endpoint import LocalResource


class SeparateResource(LocalResource):
    """
    This class implements a 'separate' resource for demonstration purposes.
    Defines a resource that returns a response in a separate CoAP Message
    """
    def __init__(self):
        """ generated source for method __init__ """
        super(SeparateResource, self).__init__("separate")
        self.title = "GET a response in a separate CoAP Message"
        self.resourceType = "SepararateResponseTester"

    def performGET(self, request):
        """ generated source for method performGET """
        #  we know this stuff may take longer...
        #  promise the client that this request will be acted upon
        #  by sending an Acknowledgement
        request.accept()
        #  do the time-consuming computation
        try:
            Thread.sleep(1000)
        except InterruptedException as e:
            pass

        response = Response(CodeRegistry.RESP_CONTENT)

        response.payload = "This message was sent by a separate response."
        response.payload += "Your client will need to acknowledge it,"
        response.payload += "otherwise it will be retransmitted."
        request.respond(response)  # complete the request