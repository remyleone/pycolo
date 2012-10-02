# coding=utf-8
from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo import mediaTypeRegistry
from pycolo.endpoint import LocalResource


class DeviceName(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    name = "IPSO Server"

    def __init__(self):
        """ generated source for method __init__ """
        self.title = "Name"
        self.resourceType = "ipso:dev-n"
        self.interfaceDescription = "core#p"
        self.address = "dev/n"

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, \
                        self.name, \
                        mediaTypeRegistry["TEXT_PLAIN"])

    def performPUT(self, request):
        """ generated source for method performPUT """
        if request.contentType != mediaTypeRegistry["TEXT_PLAIN"]:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "text/plain only")
            return
        self.name = request.payload
        #  complete the request
        request.respond(CodeRegistry.RESP_CHANGED)
