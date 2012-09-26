#!/usr/bin/env python
""" generated source for module SeparateResource """
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

import ch.ethz.inf.vs.californium.coap.GETRequest

import ch.ethz.inf.vs.californium.coap.Response

import ch.ethz.inf.vs.californium.endpoint.LocalResource

# 
#  * This class implements a 'separate' resource for demonstration purposes.
#  * 
#  * Defines a resource that returns a response in a separate CoAP Message
#  *  
#  * @author Dominique Im Obersteg & Daniel Pauli
#  * @version 0.1
#  * 
#  
class SeparateResource(LocalResource):
    """ generated source for class SeparateResource """
    def __init__(self):
        """ generated source for method __init__ """
        super(SeparateResource, self).__init__("separate")
        setTitle("GET a response in a separate CoAP Message")
        setResourceType("SepararateResponseTester")

    def performGET(self, request):
        """ generated source for method performGET """
        #  we know this stuff may take longer...
        #  promise the client that this request will be acted upon
        #  by sending an Acknowledgement
        request.accept()
        #  do the time-consuming computation
        try:
            Thread.sleep(1000)
        except InterruptedException as e:
            pass
        #  create response
        response = Response(CodeRegistry.RESP_CONTENT)
        #  set payload
        response.setPayload("This message was sent by a separate response.\n" + "Your client will need to acknowledge it, otherwise it will be retransmitted.")
        #  complete the request
        request.respond(response)

