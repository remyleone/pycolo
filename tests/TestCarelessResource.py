# coding=utf-8

from pycolo import Resource


class CarelessResource(Resource):
    """
    This class implements a 'separate' resource for demonstration purposes.
    Defines a resource that returns a response in a separate CoAP Message
    """
    def __init__(self, title="This resource will ACK anything, but never send a separate response", resourceType="SepararateResponseTester"):
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