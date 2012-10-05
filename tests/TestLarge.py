# coding=utf-8
from pycolo import codes, Resource

from pycolo.codes import mediaCodes


class Large(Resource):
    """
    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.
    """
    def __init__(self):
        self.title = "Large resource"
        self.resourceType = "block"

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
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
        request.respond(codes.RESP_CONTENT, str(builder), mediaCodes.text)
