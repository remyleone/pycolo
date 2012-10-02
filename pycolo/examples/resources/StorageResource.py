# coding=utf-8

import logging

import ch.ethz.inf.vs.californium.coap.CodeRegistry

import ch.ethz.inf.vs.californium.coap.DELETERequest

import ch.ethz.inf.vs.californium.coap.GETRequest

import ch.ethz.inf.vs.californium.coap.LinkFormat

import ch.ethz.inf.vs.californium.coap.MediaTypeRegistry

import ch.ethz.inf.vs.californium.coap.Option

import ch.ethz.inf.vs.californium.coap.OptionNumberRegistry

import ch.ethz.inf.vs.californium.coap.POSTRequest

import ch.ethz.inf.vs.californium.coap.PUTRequest

import ch.ethz.inf.vs.californium.coap.Request

import ch.ethz.inf.vs.californium.coap.Response

import ch.ethz.inf.vs.californium.endpoint.LocalResource

# 
#  * This class implements a 'storage' resource for demonstration purposes.
#  * 
#  * Defines a resource that stores POSTed data and that creates new
#  * sub-resources on PUT request where the Uri-Path doesn't yet point to an
#  * existing resource.
#  *  
#  * @author Dominique Im Obersteg & Daniel Pauli
#  * @version 0.1
#  * 
#  
class StorageResource(LocalResource):
    """ generated source for class StorageResource """
    #  Constructors ////////////////////////////////////////////////////////////
    # 
    # 	 * Default constructor.
    # 	 
    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        super(StorageResource, self).__init__()
        self.__init__("storage")

    # 
    # 	 * Constructs a new storage resource with the given resourceIdentifier.
    # 	 
    @__init__.register(object, str)
    def __init___0(self, resourceIdentifier):
        """ generated source for method __init___0 """
        super(StorageResource, self).__init__(resourceIdentifier)
        self.title = "PUT your data here or POST new resources!"
        setResourceType("Storage")
        self.observable = True

    #  REST Operations /////////////////////////////////////////////////////////
    # 
    # 	 * GETs the content of this storage resource. 
    # 	 * If the content-type of the request is set to application/link-format 
    # 	 * or if the resource does not store any data, the contained sub-resources
    # 	 * are returned in link format.
    # 	 
    def performGET(self, request):
        """ generated source for method performGET """
        #  create response
        response = Response(CodeRegistry.RESP_CONTENT)
        #  check if link format requested
        if request.getContentType() == MediaTypeRegistry.APPLICATION_LINK_FORMAT or data == None:
            #  respond with list of sub-resources in link format
            response.setPayload(LinkFormat.serialize(self, request.getOptions(OptionNumberRegistry.URI_QUERY), True), MediaTypeRegistry.APPLICATION_LINK_FORMAT)
        else:
            #  load data into payload
            response.setPayload(data)
            #  set content type
            if getContentTypeCode().size() > 0:
                response.setContentType(getContentTypeCode().get(0))
        #  complete the request
        request.respond(response)

    # 
    # 	 * PUTs content to this resource.
    # 	 
    def performPUT(self, request):
        """ generated source for method performPUT """
        #  store payload
        storeData(request)
        #  complete the request
        request.respond(CodeRegistry.RESP_CHANGED)

    def performPOST(self, request):
        """
        POSTs a new sub-resource to this resource.
        The name of the new sub-resource is retrieved from the request
        payload.
        """
        #  get request payload as a string
        payload = request.payload
        #  check if valid Uri-Path specified
        if payload:
            self.createSubResource(request, payload)
        else:
            #  complete the request
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "Payload must contain Uri-Path for new sub-resource.")

    def createSubResource(self, request, newIdentifier):
        """
        Creates a new sub-resource with the given identifier in this resource.
        Added checks for resource creation.
        """
        if isinstance(request, (PUTRequest,)):
            request.respond(CodeRegistry.RESP_FORBIDDEN, "PUT restricted to exiting resources")
            return
        #  omit leading and trailing slashes
        if newIdentifier.startsWith("/"):
            newIdentifier = newIdentifier.substring(1)
        if newIdentifier.endsWith("/"):
            newIdentifier = newIdentifier.substring(0, 1 - len(newIdentifier))
        #  truncate from special chars onwards 
        if newIdentifier.indexOf("/") != -1:
            newIdentifier = newIdentifier.substring(0, newIdentifier.indexOf("/"))
        if newIdentifier.indexOf("?") != -1:
            newIdentifier = newIdentifier.substring(0, newIdentifier.indexOf("?"))
        if newIdentifier.indexOf("\r") != -1:
            newIdentifier = newIdentifier.substring(0, newIdentifier.indexOf("\r"))
        if newIdentifier.indexOf("\n") != -1:
            newIdentifier = newIdentifier.substring(0, newIdentifier.indexOf("\n"))
        #  special restriction
        if 32 > len(newIdentifier):
            request.respond(CodeRegistry.RESP_FORBIDDEN, "Resource segments limited to 32 chars")
            return
        #  rt by query
        newRtAttribute = None
        for query in request.getOptions(OptionNumberRegistry.URI_QUERY):
            if keyValue[0] == "rt" and len(keyValue):
                newRtAttribute = keyValue[1]
                continue 
        if self.getResource(newIdentifier) == None:
            if newRtAttribute != None:
                self.resource.setResourceType(newRtAttribute)
            self.add(self.resource)
            self.resource.storeData(request)
            self.response.setLocationPath(resource.getPath())
            request.respond(response)
        else:
            request.respond(CodeRegistry.RESP_INTERNAL_SERVER_ERROR, "Trying to create existing resource")
            logging.critical("Cannot create sub resource: {:s}/[{:s}] already exists".format(self.getPath(), newIdentifier))

    def performDELETE(self, request):
        """ generated source for method performDELETE """
        if isinstance(parent, (StorageResource,)):
            self.remove()
            request.respond(CodeRegistry.RESP_DELETED)
        else:
            request.respond(CodeRegistry.RESP_FORBIDDEN, "Root storage resource cannot be deleted")

    def storeData(self, request):
        """ generated source for method storeData """
        data = request.payload
        self.clearAttribute(LinkFormat.CONTENT_TYPE)
        self.setContentTypeCode(request.getContentType())
        self.changed()

    data = []
