# coding=utf-8

from pycolo import Response, codes
from pycolo.codes import mediaCodes
from pycolo.Resource import Resource



class LargeCreate(Resource):
    """
    This resource implements a test of specification for the
    ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.
    """

    data = None
    dataCt = -1

    def __init__(self):
        """
        Constructs a new storage resource with the given resourceIdentifier.
        """
        super(LargeCreate, self).__init__()
        self.__init__("large-create")
        self.title = "Large resource that can be created using POST method"
        self.resourceType = "block"

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        response = None
        if not self.data:
            response = Response(codes.RESP_CONTENT)
            response.setPayload("Nothing posted yet", mediaCodes.text)
        else:
            #  content negotiation
            supported.add(self.dataCt)
            if ct = MediaTypeRegistry.contentNegotiation(self.dataCt, supported, request.getOptions(OptionNumberRegistry.ACCEPT))) == var = MediaTypeRegistry.UNDEFINED
            :
                request.respond(codes.RESP_NOT_ACCEPTABLE, "Accept " + MediaTypeRegistry.toString(self.dataCt))
                return
            response = Response(codes.RESP_CONTENT)

            response.payload = self.data  # load data into payload
            response.setContentType(ct)  # set content type

        request.respond(response)  # complete the request

    def performPOST(self, request):
        """ POST content to create this resource.
        :param request:
        """
        if request.getContentType() == MediaTypeRegistry.UNDEFINED:
            request.respond(codes.RESP_BAD_REQUEST, "Content-Type not set")
            return
        #  store payload
        storeData(request)
        #  create new response
        response = Response(codes.RESP_CREATED)
        #  inform client about the location of the new resource
        response.setLocationPath("/nirvana")
        #  complete the request
        request.respond(response)

    def performDELETE(self, request):
        """ DELETE the data and act as resouce was deleted.
        :param request:
        """
        #  delete
        self.data = None
        #  complete the request
        request.respond(Response(codes.RESP_DELETED))

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
