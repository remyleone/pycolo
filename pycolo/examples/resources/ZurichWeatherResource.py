#!/usr/bin/env python
""" generated source for module ZurichWeatherResource """
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
import java.io.BufferedReader

import java.io.IOException

import java.io.InputStreamReader

import java.io.StringReader

import java.net.URL

import java.util.ArrayList

import java.util.List

import java.util.Timer

import java.util.TimerTask

import javax.xml.parsers.DocumentBuilderFactory

import javax.xml.parsers.ParserConfigurationException

import org.w3c.dom.Document

import org.w3c.dom.Node

import org.w3c.dom.NodeList

import org.xml.sax.InputSource

import org.xml.sax.SAXException

import ch.ethz.inf.vs.californium.coap.CodeRegistry

import ch.ethz.inf.vs.californium.coap.GETRequest

import ch.ethz.inf.vs.californium.coap.MediaTypeRegistry

import ch.ethz.inf.vs.californium.coap.OptionNumberRegistry

import ch.ethz.inf.vs.californium.coap.Response

import ch.ethz.inf.vs.californium.endpoint.LocalResource

# 
#  * Defines a resource that returns the current weather on a GET request.
#  * 
#  * @author Dominique Im Obersteg, Daniel Pauli, and Matthias Kovatsch
#  
class ZurichWeatherResource(LocalResource):
    """ generated source for class ZurichWeatherResource """
    WEATHER_MAX_AGE = 300000

    #  5min
    #  The current weather information represented as string
    weatherXML = str()
    weatherPLAIN = str()
    supported = ArrayList()

    # 
    # 	 * Constructor for a new ZurichWeatherResource
    # 	 
    def __init__(self):
        """ generated source for method __init__ """
        super(ZurichWeatherResource, self).__init__("weatherResource")
        setTitle("GET the current weather in zurich")
        setResourceType("ZurichWeather")
        isObservable(True)
        self.supported.add(MediaTypeRegistry.TEXT_PLAIN)
        self.supported.add(MediaTypeRegistry.APPLICATION_XML)
        for ct in supported:
            setContentTypeCode(ct)
        getZurichWeather()
        #  Set timer task scheduling
        timer = Timer()
        timer.schedule(ZurichWeatherTask(), 0, self.WEATHER_MAX_AGE)

    class ZurichWeatherTask(TimerTask):
        """ generated source for class ZurichWeatherTask """
        def run(self):
            """ generated source for method run """
            weatherOLD = str(self.weatherXML)
            getZurichWeather()
            if not weatherOLD == self.weatherXML:
                changed()

    def getZurichWeather(self):
        """ generated source for method getZurichWeather """
        url = URL()
        rawWeather = ""
        try:
            url = URL("http://weather.yahooapis.com/forecastrss?w=12893366")
            while (inputLine = in_.readLine()) != None:
                rawWeather += inputLine + "\n"
            in_.close()
        except IOException as e:
            System.err.println("getZurichWeather IOException")
            e.printStackTrace()
        self.weatherPLAIN = parseWeatherXML(rawWeather)
        self.weatherXML = rawWeather

    # 
    # 	 * Parses a given string describing an XML document
    # 	 
    def parseWeatherXML(self, input):
        """ generated source for method parseWeatherXML """
        result = ""
        try:
            result = traverseXMLTree(xmlDocument)
        except SAXException as e:
            System.err.println("parseWeatherXML SAXException")
            e.printStackTrace()
        except IOException as e:
            System.err.println("parseWeatherXML IOException")
            e.printStackTrace()
        except ParserConfigurationException as e:
            System.err.println("parseWeatherXML ParserConfigurationException")
            e.printStackTrace()
        return result

    # 
    # 	 * Traverses the XML structure and parses relevant data
    # 	 * 
    # 	 * @param node The root node of the document
    # 	 * 
    # 	 * @return A formatted string containing the parsed data
    # 	 
    def traverseXMLTree(self, node):
        """ generated source for method traverseXMLTree """
        #  Use stringbuilder to build result string more efficiently
        weatherResult = StringBuilder()
        #  Get location information
        if node.getNodeName() == "yweather:location":
            weatherResult.append("------------------------")
            weatherResult.append("\n  Location Information\n")
            weatherResult.append("------------------------")
            weatherResult.append("\n")
            #  Get all location information attributes and append the
            #  information to the string
            while j < node.getAttributes().getLength():
                weatherResult.append("   ")
                weatherResult.append(node.getAttributes().item(j).getNodeName())
                weatherResult.append(": ")
                weatherResult.append(node.getAttributes().item(j).getNodeValue())
                weatherResult.append("\n")
                j += 1
            weatherResult.append("------------------------\n\n")
        elif node.getNodeName() == "yweather:units":
            weatherResult.append("------------------------")
            weatherResult.append("\n   Unit Information\n")
            weatherResult.append("------------------------")
            weatherResult.append("\n")
            while j < node.getAttributes().getLength():
                weatherResult.append("   ")
                weatherResult.append(node.getAttributes().item(j).getNodeName())
                weatherResult.append(": ")
                weatherResult.append(node.getAttributes().item(j).getNodeValue())
                weatherResult.append("\n")
                j += 1
            weatherResult.append("------------------------\n\n")
        elif node.getNodeName() == "yweather:forecast":
            weatherResult.append("-----------------------------")
            weatherResult.append("\n Weather Forecast: ")
            weatherResult.append(node.getAttributes().item(1).getNodeValue())
            weatherResult.append("\n")
            weatherResult.append("-----------------------------")
            weatherResult.append("\n")
            while j < node.getAttributes().getLength():
                weatherResult.append("   ")
                weatherResult.append(node.getAttributes().item(j).getNodeName())
                weatherResult.append(": ")
                weatherResult.append(node.getAttributes().item(j).getNodeValue())
                weatherResult.append("\n")
                j += 1
            weatherResult.append("-----------------------------\n\n")
        if node.hasChildNodes():
            while i < children.getLength():
                weatherResult.append(self.traverseXMLTree(children.item(i)))
                i += 1
        return weatherResult.__str__()

    def performGET(self, request):
        """ generated source for method performGET """
        ct = MediaTypeRegistry.TEXT_PLAIN
        if (ct = MediaTypeRegistry.contentNegotiation(ct, self.supported, request.getOptions(OptionNumberRegistry.ACCEPT))) == MediaTypeRegistry.UNDEFINED:
            request.respond(CodeRegistry.RESP_NOT_ACCEPTABLE, "Supports text/plain and application/xml")
            return
        response = Response(CodeRegistry.RESP_CONTENT)
        response.setMaxAge(self.WEATHER_MAX_AGE / 1000)
        if ct == MediaTypeRegistry.APPLICATION_XML:
            response.setPayload(self.weatherXML, MediaTypeRegistry.APPLICATION_XML)
        else:
            response.setPayload(self.weatherPLAIN, MediaTypeRegistry.TEXT_PLAIN)
        request.respond(response)

