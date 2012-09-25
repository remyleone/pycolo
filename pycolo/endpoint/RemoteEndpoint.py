# coding=utf-8
from urllib.parse import urlparse

from pycolo.coap import Communicator
from pycolo.endpoint import Endpoint


class RemoteEndpoint(Endpoint):
    """
    The class RemoteEndpoint is currently an unimplemented skeleton for a
    client stub to access a {@link LocalEndpoint} at the server.
    """
    @classmethod
    def fromURI(cls, uri):
        try:
            return RemoteEndpoint(URI(uri))
        except URISyntaxException as e:
            System.out.printf("[%s] Failed to create RemoteEndpoint from URI: %s\n", "JCoAP", e.getMessage())
            return None

    def __init__(self, uri):
        super(RemoteEndpoint, self).__init__()
        #  initialize communicator
        Communicator.setupDeamon(True)
        Communicator.getInstance().registerReceiver(self)
        self.uri = uri

    def execute(self, request):
        if request != None:
            request.setURI(self.uri)
            #  execute the request
            request.execute()

    uri = URI()

    def handleRequest(self, request):
        pass

    def handleResponse(self, response):
        pass
