# coding=utf-8

import logging
from pycolo import Resource
from pycolo import Response
from pycolo.codes import mediaCodes
from pycolo.codes import codes

class StorageResource(Resource):
    """
    This class implements a 'storage' resource for demonstration purposes.

    Defines a resource that stores POSTed data and that creates new
    sub-resources on PUT request where the Uri-Path doesn't yet point to an
    existing resource.
    """

    def __init__(self):
        """
        Constructs a new storage resource with the given resourceIdentifier.
        :return:
        """
        super(StorageResource, self).__init__()
        self.__init__("storage")
        self.title = "PUT your data here or POST new resources!"
        self.setResourceType("Storage")
        self.observable = True


    def performGET(self, request):
        """
        GETs the content of this storage resource.
        If the content-type of the request is set to application/link-format
        or if the resource does not store any data, the contained sub-resources
        are returned in link format.
        """
        #  create response
        response = Response(CodeRegistry.RESP_CONTENT)
        #  check if link format requested
        if request.contentType == mediaCodes.APPLICATION_LINK_FORMAT or not self.data:
            #  respond with list of sub-resources in link format
            response.setPayload(LinkFormat.serialize(self, request.getOptions(OptionNumberRegistry.URI_QUERY), True), MediaTypeRegistry.APPLICATION_LINK_FORMAT)
        else:
            #  load data into payload
            response.payload = self.data
            #  set content type
            if getContentTypeCode().size() > 0:
                response.setContentType(getContentTypeCode().get(0))
        #  complete the request
        request.respond(response)

    def performPUT(self, request):
        """
        PUTs content to this resource.
        """
        #  store payload
        self.storeData(request)
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
            request.respond(codes.RESP_BAD_REQUEST, "Payload must contain Uri-Path for new sub-resource.")

    def createSubResource(self, request, newIdentifier):
        """
        Creates a new sub-resource with the given identifier in this resource.
        Added checks for resource creation.
        """
        if isinstance(request, (PUTRequest,)):
            request.respond(codes.RESP_FORBIDDEN, "PUT restricted to exiting resources")
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
            request.respond(codes.RESP_FORBIDDEN, "Resource segments limited to 32 chars")
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
        if isinstance(self.parent, (StorageResource,)):
            self.remove()
            request.respond(codes.RESP_DELETED)
        else:
            request.respond(codes.RESP_FORBIDDEN, "Root storage resource cannot be deleted")

    def storeData(self, request):
        """ generated source for method storeData """
        data = request.payload
        self.clearAttribute(LinkFormat.CONTENT_TYPE)
        self.setContentTypeCode(request.getContentType())
        self.changed()

    data = []
