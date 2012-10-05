# coding=utf-8
from pycolo import link, Response, codes
from pycolo.Resource import Resource
from pycolo.codes import mediaCodes
from pycolo.codes import options

class DiscoveryResource(Resource):
    """ This class implements the CoAP /.well-known/core resource. """
    #  The default resource identifier for resource discovery. 
    DEFAULT_IDENTIFIER = ".well-known/core"

    #  The root resource of the endpoint used for recursive Link-Format generation. 
    root = Resource()

    def __init__(self, rootResource):
        """ generated source for method __init__ """
        super(DiscoveryResource, self).__init__(True)
        #  hidden
        self.contentType(mediaCodes.APPLICATION_LINK_FORMAT)
        self.root = rootResource

    def performGET(self, request):
        """ generated source for method performGET """
        #  create response
        response = Response(codes.RESP_CONTENT)
        #  get filter query
        query = request.getOptions(options.URI_QUERY)
        #  return resources in link-format
        response.setPayload(link.serialize(self.root, query, True), mediaCodes.APPLICATION_LINK_FORMAT)
        #  complete the request
        request.respond(response)
