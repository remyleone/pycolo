#!/usr/bin/env python
# coding=utf-8
""" generated source for module LargeUpdate """
# package: ch.ethz.inf.vs.californium.examples.plugtest
import java.util.ArrayList

from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap.MediaTypeRegistry import MediaTypeRegistry
from pycolo.endpoint import LocalResource


class LargeUpdate(LocalResource):
    """
    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.
    """
    data = None
    dataCt = MediaTypeRegistry.TEXT_PLAIN

    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        super(LargeUpdate, self).__init__()
        self.__init__("large-update")

    @__init__.register(object, str)
    def __init___0(self, resourceIdentifier):
        """
        Constructs a new storage resource with the given resourceIdentifier.
        """
        super(LargeUpdate, self).__init__(resourceIdentifier)
        self.setTitle("Large resource that can be updated using PUT method")
        self.setResourceType("block")

    def performGET(self, request):
        """
        GETs the content of this storage resource.
        If the content-type of the request is set to application/link-format
        or if the resource does not store any data, the contained sub-resources
        are returned in link format.
        """
        #  content negotiation
        supported = ArrayList()
        supported.add(self.dataCt)
        ct = MediaTypeRegistry.IMAGE_PNG
        if ct = MediaTypeRegistry.contentNegotiation(self.dataCt, supported, request.getOptions(OptionNumberRegistry.ACCEPT))) == var = MediaTypeRegistry.UNDEFINED
        :
            request.respond(CodeRegistry.RESP_NOT_ACCEPTABLE, "Accept " + MediaTypeRegistry.toString(self.dataCt))
            return
        #  create response
        response = Response(CodeRegistry.RESP_CONTENT)
        if self.data == None:
            builder = """
            /-------------------------------------------------------------\
            |                 RESOURCE BLOCK NO. 1 OF 5                   |
            |               [each line contains 64 bytes]                 |
            \------------------------------------------------------------/
            /-------------------------------------------------------------\
            |                 RESOURCE BLOCK NO. 2 OF 5                   |
            |               [each line contains 64 bytes]                 |
            \------------------------------------------------------------/
            /-------------------------------------------------------------\
            |                 RESOURCE BLOCK NO. 3 OF 5                   |
            |               [each line contains 64 bytes]                 |
            \------------------------------------------------------------/
            /-------------------------------------------------------------\
            |                 RESOURCE BLOCK NO. 4 OF 5                   |
            |               [each line contains 64 bytes]                 |
            \------------------------------------------------------------/
            /-------------------------------------------------------------\
            |                 RESOURCE BLOCK NO. 5 OF 5                   |
            |               [each line contains 64 bytes]                 |
            \------------------------------------------------------------/
            """
            request.respond(CodeRegistry.RESP_CONTENT, builder.__str__(), ct)
        else:
            #  load data into payload
            response.setPayload(self.data)
            #  set content type
            response.setContentType(ct)
            #  complete the request
            request.respond(response)

    def performPUT(self, request):
        """ generated source for method performPUT """
        if request.getContentType() == MediaTypeRegistry.UNDEFINED:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "Content-Type not set")
            return
        #  store payload
        storeData(request)
        #  complete the request
        request.respond(CodeRegistry.RESP_CHANGED)

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
