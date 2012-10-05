# coding=utf-8
from pycolo import codes, LocalResource

from pycolo.coap import GETRequest


class LargeResource(LocalResource):
    """
    This class implements a resource that returns a larger amount of
    data on GET requests in order to test blockwise transfers.
    """
    def __init__(self):
        """ generated source for method __init__ """
        super(LargeResource, self).__init__("large")
        self.title = "This is a large resource for testing block-wise transfer"
        self.resourceType "BlockWiseTransferTester"

    def performGET(self, request):
        """
        TODO: Cleaning this text
        """
        builder = """
        /-------------------------------------------------------------\\"
        |                 RESOURCE BLOCK NO. 1 OF 8                   |
        |               [each line contains 64 bytes]                 |
        \\-------------------------------------------------------------/
        /-------------------------------------------------------------\\
        |                 RESOURCE BLOCK NO. 2 OF 8                   |\
        |               [each line contains 64 bytes]                 |\
        \\-------------------------------------------------------------/
        /-------------------------------------------------------------\\
        |                 RESOURCE BLOCK NO. 3 OF 8                   |
        |               [each line contains 64 bytes]                 |
        \\-------------------------------------------------------------/
        /-------------------------------------------------------------\\
        |                 RESOURCE BLOCK NO. 4 OF 8                   |
        |               [each line contains 64 bytes]                 |
        \\-------------------------------------------------------------/
        /-------------------------------------------------------------\\
        |                 RESOURCE BLOCK NO. 5 OF 8                   |
        |               [each line contains 64 bytes]                 |
        \\-------------------------------------------------------------/
        /-------------------------------------------------------------\\
        |                 RESOURCE BLOCK NO. 6 OF 8                   |
        |               [each line contains 64 bytes]                 |
        \\-------------------------------------------------------------/
        /-------------------------------------------------------------\\
        |                 RESOURCE BLOCK NO. 7 OF 8                   |
        |               [each line contains 64 bytes]                 |
        \\-------------------------------------------------------------/"
        /-------------------------------------------------------------\\"
        |                 RESOURCE BLOCK NO. 8 OF 8                   |
        |               [each line contains 64 bytes]                 |
        \\------------------------------------------------------------/"
	"""
        request.respond(codes.RESP_CONTENT, builder.__str__())

