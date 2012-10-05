# coding=utf-8

from pycolo.codes import codes
from pycolo.codes import mediaCodes
from pycolo import Response
from pycolo import Resource

class LongPath(Resource):
    """
    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.
    """
    def __init__(self):
        self.title = "Long path resource"

    def performGET(self, request):
        """ generated source for method performGET """
        #  create response
        response = Response(codes.RESP_CONTENT)
        payload = "Type: {:d} ({:s})\nCode: {:d} ({:s})\nMID: {:d}".format(\
            request.getType().ordinal(),\
            request.typeString(),\
            request.code,\
            request.MID)
        #  set payload
        response.payload = payload
        response.contentType = mediaCodes.text
        #  complete the request
        request.respond(response)

