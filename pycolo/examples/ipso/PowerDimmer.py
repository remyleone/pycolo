# coding=utf-8
from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.endpoint import LocalResource
from pycolo import mediaTypeRegistry


class PowerDimmer(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    percent = 100

    def __init__(self):
        """ generated source for method __init__ """
        super(PowerDimmer, self).__init__("pwr/dim")
        self.title = "Load Dimmer"
        self.resourceType = "ipso:pwr-dim"
        self.interfaceDescription = "core#a"
        self.observable = True

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, \
                        int(self.percent), \
                        mediaTypeRegistry["TEXT_PLAIN"])

    def performPUT(self, request):
        """ generated source for method performPUT """
        if request.contentType != mediaTypeRegistry["TEXT_PLAIN"]:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "text/plain only")
            return
        pl = int(request.payload)
        if 0 <= pl <= 100:
            if self.percent == pl:
                return
            self.percent = pl
            request.respond(CodeRegistry.RESP_CHANGED)
            self.changed()
        else:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "use 0-100")
