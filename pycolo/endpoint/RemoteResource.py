# coding=utf-8
from pycolo.coap import LinkFormat
from pycolo.endpoint import Resource


class RemoteResource(Resource):
    """
    The class RemoteResource is currently an unimplemented skeleton for a
    client stub to access a {@link LocalResource} at the server.
    So far, it can be used as a discovery cache.
    """
    def __init__(self, resourceIdentifier):
        """ generated source for method __init__ """
        super(RemoteResource, self).__init__(resourceIdentifier)

    @classmethod
    def newRoot(cls, linkFormat):
        """ generated source for method newRoot """
        return LinkFormat.parse(linkFormat)

    def createSubResource(self, request, newIdentifier):
        pass

    def performDELETE(self, request):
        pass

    def performGET(self, request):
        pass

    def performPOST(self, request):
        pass

    def performPUT(self, request):
        pass
