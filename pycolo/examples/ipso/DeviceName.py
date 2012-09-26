# coding=utf-8
from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap.MediaTypeRegistry import MediaTypeRegistry
from pycolo.endpoint import LocalResource


class DeviceName(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    name = "IPSO Server"

    def __init__(self):
        """ generated source for method __init__ """
        super(DeviceName, self).__init__("dev/n")
        self.setTitle("Name")
        self.setResourceType("ipso:dev-n")
        self.setInterfaceDescription("core#p")

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, self.name, MediaTypeRegistry.TEXT_PLAIN)

    def performPUT(self, request):
        """ generated source for method performPUT """
        if request.getContentType() != MediaTypeRegistry.TEXT_PLAIN:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "text/plain only")
            return
        self.name = request.getPayloadString()
        #  complete the request
        request.respond(CodeRegistry.RESP_CHANGED)
