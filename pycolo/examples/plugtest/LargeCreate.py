# coding=utf-8

import java.util.ArrayList

from pycolo.coap import CodeRegistry
from pycolo.coap import MediaTypeRegistry
from pycolo.coap import Response
from pycolo.endpoint import LocalResource


class LargeCreate(LocalResource):
    """
    This resource implements a test of specification for the
    ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.
    """
    #  Members ////////////////////////////////////////////////////////////////
    data = None
    dataCt = -1

    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        super(LargeCreate, self).__init__()
        self.__init__("large-create")

    @__init__.register(object, str)
    def __init___0(self, resourceIdentifier):
        """
        Constructs a new storage resource with the given resourceIdentifier.
        """
        super(LargeCreate, self).__init__(False)
        self.setTitle("Large resource that can be created using POST method")
        self.setResourceType("block")

    def performGET(self, request):
        """ generated source for method performGET """
        response = None
        if self.data == None:
            response = Response(CodeRegistry.RESP_CONTENT)
            response.setPayload("Nothing POSTed yet", MediaTypeRegistry.TEXT_PLAIN)
        else:
            #  content negotiation
            supported.add(self.dataCt)
            if ct = MediaTypeRegistry.contentNegotiation(self.dataCt, supported, request.getOptions(OptionNumberRegistry.ACCEPT))) == var = MediaTypeRegistry.UNDEFINED
            :
                request.respond(CodeRegistry.RESP_NOT_ACCEPTABLE, "Accept " + MediaTypeRegistry.toString(self.dataCt))
                return
            response = Response(CodeRegistry.RESP_CONTENT)
            #  load data into payload
            response.setPayload(self.data)
            #  set content type
            response.setContentType(ct)
        #  complete the request
        request.respond(response)

    def performPOST(self, request):
        """ POST content to create this resource. """
        if request.getContentType() == MediaTypeRegistry.UNDEFINED:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "Content-Type not set")
            return
        #  store payload
        storeData(request)
        #  create new response
        response = Response(CodeRegistry.RESP_CREATED)
        #  inform client about the location of the new resource
        response.setLocationPath("/nirvana")
        #  complete the request
        request.respond(response)

    def performDELETE(self, request):
        """ DELETE the data and act as resouce was deleted. """
        #  delete
        self.data = None
        #  complete the request
        request.respond(Response(CodeRegistry.RESP_DELETED))

    #  Internal ////////////////////////////////////////////////////////////////
    # 
    # 	 * Convenience function to store data contained in a 
    # 	 * PUT/POST-Request. Notifies observing endpoints about
    # 	 * the change of its contents.
    # 	 
    # 
    # 	private synchronized void storeData(Request request) {
    #  set payload and content type
    # 		data = request.getPayload();
    # 		dataCt = request.getContentType();
    # 		clearAttribute(LinkFormat.CONTENT_TYPE);
    # 		setContentTypeCode(dataCt);
    #  signal that resource state changed
    # 		changed();
    # 	}
    # 	

