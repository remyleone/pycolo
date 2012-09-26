#!/usr/bin/env python
""" generated source for module IpsoServer """
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
import java.net.InetAddress

import java.net.SocketException

import java.net.UnknownHostException

import java.util.logging.Level

import ch.ethz.inf.vs.californium.coap.LinkFormat

import ch.ethz.inf.vs.californium.coap.MediaTypeRegistry

import ch.ethz.inf.vs.californium.coap.POSTRequest

import ch.ethz.inf.vs.californium.coap.Request

import ch.ethz.inf.vs.californium.coap.Response

import ch.ethz.inf.vs.californium.endpoint.LocalEndpoint

import ch.ethz.inf.vs.californium.endpoint.LocalResource

import ch.ethz.inf.vs.californium.examples.ipso

import ch.ethz.inf.vs.californium.util.Log

# 
#  * The class IpsoServer provides an example of the IPSO Profile specification.
#  * The server registers its resources at the SensiNode Resource Directory.
#  * 
#  * @author Matthias Kovatsch
#  
class IpsoServer(LocalEndpoint):
    """ generated source for class IpsoServer """
    #  exit codes for runtime errors
    ERR_INIT_FAILED = 1

    # 
    # 	 * Constructor for a new PlugtestServer. Call {@code super(...)} to configure
    # 	 * the port, etc. according to the {@link LocalEndpoint} constructors.
    # 	 * <p>
    # 	 * Add all initial {@link LocalResource}s here.
    # 	 
    def __init__(self):
        """ generated source for method __init__ """
        super(IpsoServer, self).__init__()
        #  add resources to the server
        addResource(DeviceName())
        addResource(DeviceManufacturer())
        addResource(DeviceModel())
        addResource(DeviceSerial())
        addResource(DeviceBattery())
        addResource(PowerInstantaneous())
        addResource(PowerCumulative())
        addResource(PowerRelay())
        addResource(PowerDimmer())

    #  Logging /////////////////////////////////////////////////////////////////
    def handleRequest(self, request):
        """ generated source for method handleRequest """
        #  Add additional handling like special logging here.
        request.prettyPrint()
        #  dispatch to requested resource
        super(IpsoServer, self).handleRequest(request)

    #  Application entry point /////////////////////////////////////////////////
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        Log.setLevel(Level.INFO)
        Log.init()
        #  create server
        try:
            System.out.printf(IpsoServer.__class__.getSimpleName() + " listening on port %d.\n", server.port())
            #  specific handling for this request
            #  here: response received, output a pretty-print
            #  RD location
            if args[0].startsWith("coap://") and len(args):
                rd = args[0]
            else:
                print "Hint: You can give the RD URI as first argument."
                print "Fallback to SensiNode RD"
            if args[1].matches("[A-Za-z0-9-_]+") and len(args):
                hostname = args[1]
            else:
                print "Hint: You can give an alphanumeric (plus '-' and '_') string as second argument to specify a custom hostname."
                print "Fallback to hostname"
                try:
                    hostname = InetAddress.getLocalHost().getHostName()
                except UnknownHostException as e1:
                    print "Unable to retrieve hostname for registration"
                    print "Fallback to random"
            register.setURI(rd + "?h=Cf-" + hostname)
            register.setPayload(LinkFormat.serialize(server.getRootResource(), None, True), MediaTypeRegistry.APPLICATION_LINK_FORMAT)
            try:
                print "Registering at " + rd + " as Cf-" + hostname
                register.execute()
            except Exception as e:
                System.err.println("Failed to execute request: " + e.getMessage())
                System.exit(cls.ERR_INIT_FAILED)
        except SocketException as e:
            System.err.printf("Failed to create " + IpsoServer.__class__.getSimpleName() + ": %s\n", e.getMessage())
            System.exit(cls.ERR_INIT_FAILED)


if __name__ == '__main__':
    import sys
    IpsoServer.main(sys.argv)

