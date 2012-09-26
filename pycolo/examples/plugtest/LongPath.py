# coding=utf-8

from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap.MediaTypeRegistry import MediaTypeRegistry
from pycolo.coap import Response
from pycolo.endpoint import LocalResource


class LongPath(LocalResource):
    """
    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.
    """
    def __init__(self):
        """ generated source for method __init__ """
        super(LongPath, self).__init__("seg1/seg2/seg3")
        self.setTitle("Long path resource")

    def performGET(self, request):
        """ generated source for method performGET """
        #  create response
        response = Response(CodeRegistry.RESP_CONTENT)
        payload = "Type: {:d} ({:s})\nCode: {:d} ({:s})\nMID: {:d}".format(request.getType().ordinal(), request.typeString(), request.getCode(), CodeRegistry.toString(request.getCode()), request.getMID())
        #  set payload
        response.setPayload(payload)
        response.setContentType(MediaTypeRegistry.TEXT_PLAIN)
        #  complete the request
        request.respond(response)

