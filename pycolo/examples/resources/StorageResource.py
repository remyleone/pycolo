#!/usr/bin/env python
""" generated source for module StorageResource """
# 
#  * Copyright (c) 2012, Institute for Pervasive Computing, ETH Zurich.
#  * All rights reserved.
#  * 
#  * Redistribution and use in source and binary forms, with or without
#  * modification, are permitted provided that the following conditions
#  * are met:
#  * 1. Redistributions of source code must retain the above copyright
#  *    notice, this list of conditions and the following disclaimer.
#  * 2. Redistributions in binary form must reproduce the above copyright
#  *    notice, this list of conditions and the following disclaimer in the
#  *    documentation and/or other materials provided with the distribution.
#  * 3. Neither the name of the Institute nor the names of its contributors
#  *    may be used to endorse or promote products derived from this software
#  *    without specific prior written permission.
#  * 
#  * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS "AS IS" AND
#  * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
#  * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
#  * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#  * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#  * SUCH DAMAGE.
#  * 
#  * This file is part of the Californium (Cf) CoAP framework.
#  
# package: ch.ethz.inf.vs.californium.examples.resources
import java.util.logging.Logger

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
        setTitle("PUT your data here or POST new resources!")
        setResourceType("Storage")
        isObservable(True)

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

    # 
    # 	 * POSTs a new sub-resource to this resource.
    # 	 * The name of the new sub-resource is retrieved from the request
    # 	 * payload.
    # 	 
    def performPOST(self, request):
        """ generated source for method performPOST """
        #  get request payload as a string
        payload = request.getPayloadString()
        #  check if valid Uri-Path specified
        if payload != None and not payload.isEmpty():
            createSubResource(request, payload)
        else:
            #  complete the request
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "Payload must contain Uri-Path for new sub-resource.")

    # 
    # 	 * Creates a new sub-resource with the given identifier in this resource.
    # 	 * Added checks for resource creation.
    # 	 
    def createSubResource(self, request, newIdentifier):
        """ generated source for method createSubResource """
        if isinstance(request, (PUTRequest, )):
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
        if getResource(newIdentifier) == None:
            if newRtAttribute != None:
                resource.setResourceType(newRtAttribute)
            add(resource)
            resource.storeData(request)
            response.setLocationPath(resource.getPath())
            request.respond(response)
        else:
            request.respond(CodeRegistry.RESP_INTERNAL_SERVER_ERROR, "Trying to create existing resource")
            Logger.getAnonymousLogger().severe("Cannot create sub resource: {:s}/[{:s}] already exists".format(self.getPath(), newIdentifier))

    def performDELETE(self, request):
        """ generated source for method performDELETE """
        if isinstance(parent, (StorageResource, )):
            remove()
            request.respond(CodeRegistry.RESP_DELETED)
        else:
            request.respond(CodeRegistry.RESP_FORBIDDEN, "Root storage resource cannot be deleted")

    def storeData(self, request):
        """ generated source for method storeData """
        data = request.getPayload()
        clearAttribute(LinkFormat.CONTENT_TYPE)
        setContentTypeCode(request.getContentType())
        changed()

    data = []

