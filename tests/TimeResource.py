#!/usr/bin/env python
""" generated source for module TimeResource """
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
import java.text.DateFormat

import java.text.SimpleDateFormat

import java.util.Date

import java.util.Timer

import java.util.TimerTask

import ch.ethz.inf.vs.californium.coap.CodeRegistry

import ch.ethz.inf.vs.californium.coap.GETRequest

import ch.ethz.inf.vs.californium.coap.MediaTypeRegistry

import ch.ethz.inf.vs.californium.endpoint.LocalResource

# 
#  * Defines a resource that returns the current time on a GET request.
#  * It also Supports observing. 
#  *  
#  * @author Dominique Im Obersteg, Daniel Pauli, and Matthias Kovatsch
#  
class TimeResource(LocalResource):
    """ generated source for class TimeResource """
    #  The current time represented as string
    time = str()

    # 
    # 	 * Constructor for a new TimeResource
    # 	 
    def __init__(self):
        """ generated source for method __init__ """
        super(TimeResource, self).__init__("timeResource")
        setTitle("GET the current time")
        setResourceType("CurrentTime")
        isObservable(True)
        #  Set timer task scheduling
        timer = Timer()
        timer.schedule(TimeTask(), 0, 2000)

    # 
    # 	 * Defines a new timer task to return the current time
    # 	 
    class TimeTask(TimerTask):
        """ generated source for class TimeTask """
        def run(self):
            """ generated source for method run """
            self.time = getTime()
            #  Call changed to notify subscribers
            changed()

    # 
    # 	 * Returns the current time
    # 	 * 
    # 	 * @return The current time
    # 	 
    def getTime(self):
        """ generated source for method getTime """
        dateFormat = SimpleDateFormat("EEEEEEEEE, dd.MM.yyyy, HH:mm:ss")
        time = Date()
        return dateFormat.format(time)

    def performGET(self, request):
        """ generated source for method performGET """
        request.respond(CodeRegistry.RESP_CONTENT, self.time, MediaTypeRegistry.TEXT_PLAIN)

