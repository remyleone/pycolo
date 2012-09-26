#!/usr/bin/env python
""" generated source for module RTTClient """
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
import java.io.IOException

import java.net.URI

import java.net.URISyntaxException

import java.util.logging.Level

import ch.ethz.inf.vs.californium.coap.GETRequest

import ch.ethz.inf.vs.californium.coap.Request

import ch.ethz.inf.vs.californium.coap.Response

import ch.ethz.inf.vs.californium.util.Log

class RTTClient(object):
    """ generated source for class RTTClient """
    uriString = ""
    n = 1000
    sent = 0
    received = 0
    total = 0
    min = Double.MAX_VALUE
    max = 0

    # 
    # 	 * Main method of this client.
    # 	 
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        uri = None
        Log.setLevel(Level.WARNING)
        Log.init()
        if len(args):
            #  input URI from command line arguments
            try:
                uri = URI(args[0])
                cls.uriString = args[0]
            except URISyntaxException as e:
                System.err.println("Invalid URI: " + e.getMessage())
                System.exit(-1)
            if len(args):
                try:
                    cls.n = Integer.parseInt(args[1])
                except NumberFormatException as e:
                    System.err.println("Invalid number: " + e.getMessage())
                    System.exit(-1)
            Runtime.getRuntime().addShutdownHook(Thread())
            while i < cls.n:
                request.enableResponseQueue(True)
                request.setURI(uri)
                try:
                    request.execute()
                except IOException as e:
                    #  TODO Auto-generated catch block
                    e.printStackTrace()
                    System.exit(-1)
                try:
                    cls.sent += 1
                    if response != None:
                        cls.received += 1
                        if response.getRTT() > cls.max:
                            cls.max = response.getRTT()
                        if response.getRTT() < cls.min:
                            cls.min = response.getRTT()
                        if response.getRTT() < 0:
                            print "ERROR: Response untimed, time=" + response.getRTT()
                        elif request.getRetransmissioned() > 0:
                            print "WARNING: Response after retransmission, time=" + response.getRTT()
                        else:
                            print "time=" + response.getRTT() + "ms"
                        cls.total += response.getRTT()
                    else:
                        print "No response received"
                except InterruptedException as e:
                    #  TODO Auto-generated catch block
                    e.printStackTrace()
                i += 1
        else:
            #  display help
            print "Californium (Cf) RTT Client"
            print "(c) 2012, Institute for Pervasive Computing, ETH Zurich"
            print 
            print "Usage: " + RTTClient.__class__.getSimpleName() + " URI"
            print "  URI: The CoAP URI of the remote resource to measure"


if __name__ == '__main__':
    import sys
    RTTClient.main(sys.argv)

