#!/usr/bin/env python
""" generated source for module HelloWorldServer """
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
# package: ch.ethz.inf.vs.californium.examples
import java.net.SocketException

import ch.ethz.inf.vs.californium.coap.CodeRegistry

import ch.ethz.inf.vs.californium.coap.GETRequest

import ch.ethz.inf.vs.californium.endpoint.LocalEndpoint

import ch.ethz.inf.vs.californium.endpoint.LocalResource

class HelloWorldServer(LocalEndpoint):
    """ generated source for class HelloWorldServer """
    # 
    # 	 * Definition of the Hello-World Resource
    # 	 * 
    # 	 
    class HelloWorldResource(LocalResource):
        """ generated source for class HelloWorldResource """
        def __init__(self):
            """ generated source for method __init__ """
            #  set resource identifier
            super(HelloWorldResource, self).__init__("helloWorld")
            #  set display name
            setTitle("Hello-World Resource")

        def performGET(self, request):
            """ generated source for method performGET """
            #  respond to the request
            request.respond(CodeRegistry.RESP_CONTENT, "Hello World!")

    # 
    # 	 * Constructor for a new Hello-World server. Here, the resources
    # 	 * of the server are initialized.
    # 	 * 
    # 	 
    def __init__(self):
        """ generated source for method __init__ """
        super(HelloWorldServer, self).__init__()
        #  provide an instance of a Hello-World resource
        addResource(self.HelloWorldResource())

    # 
    # 	 * Application entry point.
    # 	 * 
    # 	 
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        try:
            #  create server
            print "Server listening on port " + server.port()
        except SocketException as e:
            System.err.println("Failed to initialize server: " + e.getMessage())


if __name__ == '__main__':
    import sys
    HelloWorldServer.main(sys.argv)

