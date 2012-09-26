#!/usr/bin/env python
""" generated source for module PlugtestServer """
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

import java.util.logging.Level

import ch.ethz.inf.vs.californium.coap.Request

import ch.ethz.inf.vs.californium.endpoint.Endpoint

import ch.ethz.inf.vs.californium.endpoint.LocalEndpoint

import ch.ethz.inf.vs.californium.endpoint.LocalResource

import ch.ethz.inf.vs.californium.examples.plugtest

import ch.ethz.inf.vs.californium.util.Log

# 
#  * The class PlugtestServer implements the test specification for the
#  * ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.
#  * 
#  * @author Matthias Kovatsch
#  
class PlugtestServer(LocalEndpoint):
    """ generated source for class PlugtestServer """
    #  exit codes for runtime errors
    ERR_INIT_FAILED = 1

    # 
    # 	 * the port, etc. according to the {@link LocalEndpoint} constructors.
    # 	 * <p>
    # 	 * Add all initial {@link LocalResource}s here.
    # 	 
    def __init__(self):
        """ generated source for method __init__ """
        super(PlugtestServer, self).__init__()
        #  add resources to the server
        addResource(DefaultTest())
        addResource(LongPath())
        addResource(Query())
        addResource(Separate())
        addResource(Large())
        addResource(LargeUpdate())
        addResource(LargeCreate())
        addResource(Observe())

    #  Logging /////////////////////////////////////////////////////////////////
    def handleRequest(self, request):
        """ generated source for method handleRequest """
        #  Add additional handling like special logging here.
        request.prettyPrint()
        #  dispatch to requested resource
        super(PlugtestServer, self).handleRequest(request)

    #  Application entry point /////////////////////////////////////////////////
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        Log.setLevel(Level.INFO)
        Log.init()
        #  create server
        try:
            System.out.printf(PlugtestServer.__class__.getSimpleName() + " listening on port %d.\n", server.port())
        except SocketException as e:
            System.err.printf("Failed to create " + PlugtestServer.__class__.getSimpleName() + ": %s\n", e.getMessage())
            System.exit(cls.ERR_INIT_FAILED)

PlugtestServer.# 	 * Constructor for a new PlugtestServer. Call {@code super(...)} to configure


if __name__ == '__main__':
    import sys
    PlugtestServer.main(sys.argv)

