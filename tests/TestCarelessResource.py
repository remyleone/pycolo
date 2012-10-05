# coding=utf-8

from pycolo import Resource


class CarelessResource(Resource):
    """
    This class implements a 'separate' resource for demonstration purposes.
    Defines a resource that returns a response in a separate CoAP Message
    """
    def __init__(self):
        self.title = "This resource will ACK anything, but never send a separate response"
        self.resourceType = "SepararateResponseTester"

    def performGET(self, request):
        """
        promise the client that this request will be acted upon
        by sending an Acknowledgement...
        """
        request.accept()
        #  ... and then do nothing. Pretty mean.

