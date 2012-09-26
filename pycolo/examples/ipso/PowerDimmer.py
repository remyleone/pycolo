# coding=utf-8
from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap.MediaTypeRegistry import MediaTypeRegistry
from pycolo.endpoint import LocalResource


class PowerDimmer(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    percent = 100

    @classmethod
    def getDimmer(cls):
        """ generated source for method getDimmer """
        return cls.percent

    def __init__(self):
        """ generated source for method __init__ """
        super(PowerDimmer, self).__init__("pwr/dim")
        self.setTitle("Load Dimmer")
        self.setResourceType("ipso:pwr-dim")
        self.setInterfaceDescription("core#a")
        self.isObservable(True)

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, Integer.toString(self.percent), MediaTypeRegistry.TEXT_PLAIN)

    def performPUT(self, request):
        """ generated source for method performPUT """
        if request.getContentType() != MediaTypeRegistry.TEXT_PLAIN:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "text/plain only")
            return
        pl = Integer.parseInt(request.getPayloadString())
        if 0 <= pl <= 100:
            if self.percent == pl:
                return
            self.percent = pl
            request.respond(CodeRegistry.RESP_CHANGED)
            changed()
        else:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "use 0-100")
