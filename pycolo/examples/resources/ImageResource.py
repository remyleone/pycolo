#!/usr/bin/env python
""" generated source for module ImageResource """
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
import java.io.File

import java.io.FileInputStream

import java.util.ArrayList

import java.util.List

import ch.ethz.inf.vs.californium.coap.CodeRegistry

import ch.ethz.inf.vs.californium.coap.GETRequest

import ch.ethz.inf.vs.californium.coap.MediaTypeRegistry

import ch.ethz.inf.vs.californium.coap.OptionNumberRegistry

import ch.ethz.inf.vs.californium.coap.Response

import ch.ethz.inf.vs.californium.endpoint.LocalResource

# 
#  * This class implements an "/image" resource for demonstration purposes.
#  * 
#  * Provides different representations of an image through supports content
#  * negotiation.
#  * The required files are provided in the "run" directory for the .jar version.
#  * Make sure to fix the location when running elsewhere.
#  *  
#  * @author Matthias Kovatsch
#  
class ImageResource(LocalResource):
    """ generated source for class ImageResource """
    supported = ArrayList()

    #  Constructors ////////////////////////////////////////////////////////////
    # 
    # 	 * Default constructor.
    # 	 
    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        super(ImageResource, self).__init__()
        self.__init__("image")

    # 
    # 	 * Constructs a new storage resource with the given resourceIdentifier.
    # 	 
    @__init__.register(object, str)
    def __init___0(self, resourceIdentifier):
        """ generated source for method __init___0 """
        super(ImageResource, self).__init__(resourceIdentifier)
        setTitle("GET an image with different content-types")
        setResourceType("Image")
        self.supported.add(MediaTypeRegistry.IMAGE_PNG)
        self.supported.add(MediaTypeRegistry.IMAGE_JPEG)
        self.supported.add(MediaTypeRegistry.IMAGE_GIF)
        self.supported.add(MediaTypeRegistry.IMAGE_TIFF)
        for ct in supported:
            setContentTypeCode(ct)
        setMaximumSizeEstimate(18029)
        isObservable(False)

    #  REST Operations /////////////////////////////////////////////////////////
    def performGET(self, request):
        """ generated source for method performGET """
        filename = "data/image/"
        ct = MediaTypeRegistry.IMAGE_PNG
        #  content negotiation
        if (ct = MediaTypeRegistry.contentNegotiation(ct, self.supported, request.getOptions(OptionNumberRegistry.ACCEPT))) == MediaTypeRegistry.UNDEFINED:
            request.respond(CodeRegistry.RESP_NOT_ACCEPTABLE, "Accept GIF, JPEG, PNG, or TIFF")
            return
        filename += "image." + MediaTypeRegistry.toFileExtension(ct)
        # load representation from file
        file_ = File(filename)
        if not file_.exists():
            request.respond(CodeRegistry.RESP_INTERNAL_SERVER_ERROR, "Representation not found")
            return
        # get length of file
        fileLength = int(len(file_))
        fileIn = None
        fileData = [None]*fileLength
        try:
            # open input stream from file
            fileIn = FileInputStream(file_)
            # read file into byte array
            fileIn.read(fileData)
            fileIn.close()
        except Exception as e:
            request.respond(CodeRegistry.RESP_INTERNAL_SERVER_ERROR, "IO error")
            System.err.println("/image IO error: " + e.getMessage())
            return
        #  create response
        response = Response(CodeRegistry.RESP_CONTENT)
        response.setPayload(fileData)
        #  set content type
        response.setContentType(ct)
        #  complete the request
        request.respond(response)

