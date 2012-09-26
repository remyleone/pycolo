#!/usr/bin/env python
""" generated source for module ToUpperResource """
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
import ch.ethz.inf.vs.californium.coap.CodeRegistry

import ch.ethz.inf.vs.californium.coap.MediaTypeRegistry

import ch.ethz.inf.vs.californium.coap.POSTRequest

import ch.ethz.inf.vs.californium.endpoint.LocalResource

# 
#  * This class implements a 'toUpper' resource for demonstration purposes.
#  * Defines a resource that returns a POSTed string in upper-case letters.
#  *  
#  * @author Matthias Kovtsch
#  * 
#  
class ToUpperResource(LocalResource):
    """ generated source for class ToUpperResource """
    def __init__(self):
        """ generated source for method __init__ """
        super(ToUpperResource, self).__init__("toUpper")
        setTitle("POST text here to convert it to uppercase")
        setResourceType("UppercaseConverter")

    def performPOST(self, request):
        """ generated source for method performPOST """
        if request.getContentType() != MediaTypeRegistry.TEXT_PLAIN:
            request.respond(CodeRegistry.RESP_UNSUPPORTED_MEDIA_TYPE, "Use text/plain")
            return
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, request.getPayloadString().toUpperCase(), MediaTypeRegistry.TEXT_PLAIN)

