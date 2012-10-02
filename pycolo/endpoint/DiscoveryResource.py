# coding=utf-8
from pycolo.coap import CodeRegistry
from pycolo.coap import LinkFormat
from pycolo.coap import mediaTypeRegistry
from pycolo.coap.OptionNumberRegistry import OptionNumberRegistry
from pycolo.coap import Response
from pycolo.endpoint import LocalResource


class DiscoveryResource(LocalResource):
    """ This class implements the CoAP /.well-known/core resource. """
    #  The default resource identifier for resource discovery. 
    DEFAULT_IDENTIFIER = ".well-known/core"

    #  The root resource of the endpoint used for recursive Link-Format generation. 
    root = Resource()

    def __init__(self, rootResource):
        """ generated source for method __init__ """
        super(DiscoveryResource, self).__init__(True)
        #  hidden
        setContentTypeCode(MediaTypeRegistry.APPLICATION_LINK_FORMAT)
        self.root = rootResource

    def performGET(self, request):
        """ generated source for method performGET """
        #  create response
        response = Response(CodeRegistry.RESP_CONTENT)
        #  get filter query
        query = request.getOptions(OptionNumberRegistry.URI_QUERY)
        #  return resources in link-format
        response.setPayload(LinkFormat.serialize(self.root, query, True), MediaTypeRegistry.APPLICATION_LINK_FORMAT)
        #  complete the request
        request.respond(response)
