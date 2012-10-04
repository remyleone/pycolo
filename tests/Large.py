# coding=utf-8
from pycolo import codes, LocalResource

from pycolo.coap.MediaTypeRegistry import MediaTypeRegistry


class Large(LocalResource):
    """
    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.
    """
    def __init__(self):
        """ generated source for method __init__ """
        super(Large, self).__init__("large")
        self.setTitle("Large resource")
        self.setResourceType("block")

    def performGET(self, request):
        """ generated source for method performGET """
        builder = """
        /-------------------------------------------------------------\
        |                 RESOURCE BLOCK NO. 1 OF 5                   |
        |               [each line contains 64 bytes]                 |
        \\------------------------------------------------------------/
        /-------------------------------------------------------------\
        |                 RESOURCE BLOCK NO. 2 OF 5                   |
        |               [each line contains 64 bytes]                 |
        \\------------------------------------------------------------/
        /-------------------------------------------------------------\
        |                 RESOURCE BLOCK NO. 3 OF 5                   |
        |               [each line contains 64 bytes]                 |
        \\------------------------------------------------------------/
        /-------------------------------------------------------------\
        |                 RESOURCE BLOCK NO. 4 OF 5                   |
        |               [each line contains 64 bytes]                 |
        \\------------------------------------------------------------/
        /-------------------------------------------------------------\
        |                 RESOURCE BLOCK NO. 5 OF 5                   |
        |               [each line contains 64 bytes]                 |
        \\------------------------------------------------------------/
        """
        request.respond(codes.RESP_CONTENT, builder.__str__(), MediaTypeRegistry.TEXT_PLAIN)
