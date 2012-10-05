# coding=utf-8

from pycolo import Resource
from pycolo.codes import mediaCodes
from pycolo.codes import codes

class ToUpperResource(Resource):
    """
    This class implements a 'toUpper' resource for demonstration purposes.
    Defines a resource that returns a POSTed string in upper-case letters.
    """
    def __init__(self):
        self.title = "POST text here to convert it to uppercase"
        self.resourceType = "UppercaseConverter"

    def performPOST(self, request):

        if request.contentType != mediaCodes.TEXT_PLAIN:
            request.respond(codes.RESP_UNSUPPORTED_MEDIA_TYPE, "Use text/plain")
            return
        #  complete the request
        request.respond(codes.RESP_CONTENT, request.payload.upper(), mediaCodes.TEXT_PLAIN)

