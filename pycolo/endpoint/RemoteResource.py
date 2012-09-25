# coding=utf-8
from pycolo.coap import LinkFormat


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
        """ generated source for method createSubResource """
        #  TODO Auto-generated method stub

    def performDELETE(self, request):
        """ generated source for method performDELETE """
        #  TODO Auto-generated method stub

    def performGET(self, request):
        """ generated source for method performGET """
        #  TODO Auto-generated method stub

    def performPOST(self, request):
        """ generated source for method performPOST """
        #  TODO Auto-generated method stub

    def performPUT(self, request):
        """ generated source for method performPUT """
        #  TODO Auto-generated method stub
