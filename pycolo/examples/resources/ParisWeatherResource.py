# coding=utf-8

import json
import logging

from pycolo.coap import CodeRegistry
from pycolo.coap import GETRequest
from pycolo.coap import mediaTypeRegistry
from pycolo.coap import OptionNumberRegistry
from pycolo.coap import Response
from pycolo.endpoint import LocalResource


class ParisWeatherResource(LocalResource):
    """
    Defines a resource that returns the current weather on a GET request.
    """
    
    def __init__(self):
        """
        Constructor for a new ParisWeatherResource
        """
        super(ZurichWeatherResource, self).__init__("weatherResource")
        self.title = "GET the current weather in Paris"
        self.setResourceType("ZurichWeather")
        self.observable = True
        self.supported.add(MediaTypeRegistry.TEXT_PLAIN)
        self.supported.add(MediaTypeRegistry.APPLICATION_XML)
        for ct in supported:
            self.setContentTypeCode(ct)
        self.getParisWeather()
        #  Set timer task scheduling
        timer = Timer()
        timer.schedule(ZurichWeatherTask(), 0, self.WEATHER_MAX_AGE)

    class ParisWeatherTask(TimerTask):
        """ generated source for class ZurichWeatherTask """
        def run(self):
            """ generated source for method run """
            weatherOLD = str(self.weatherXML)
            getZurichWeather()
            if not weatherOLD == self.weatherXML:
                changed()

    def getParisWeather(self):
        rawWeather = ""
        try:
            url = URL("http://openweathermap.org/data/2.1/find/city?lat=48.8566140&lon=2.3522219&cnt=1")
            while (inputLine=in_.readLine()) != None:
                rawWeather += inputLine + "\n"
            in_.close()
        except IOException as e:
            logging.critical("getParisWeather IOException")
            e.printStackTrace()
        self.weatherPLAIN = parseWeatherXML(rawWeather)
        self.weatherXML = rawWeather


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
        if (ct=MediaTypeRegistry.contentNegotiation(ct, self.supported, request.getOptions(OptionNumberRegistry.ACCEPT))) == MediaTypeRegistry.UNDEFINED:
            request.respond(CodeRegistry.RESP_NOT_ACCEPTABLE, "Supports text/plain and application/xml")
            return
        response = Response(CodeRegistry.RESP_CONTENT)
        response.setMaxAge(self.WEATHER_MAX_AGE / 1000)
        if ct == MediaTypeRegistry.APPLICATION_XML:
            response.setPayload(self.weatherXML, MediaTypeRegistry.APPLICATION_XML)
        else:
            response.setPayload(self.weatherPLAIN, MediaTypeRegistry.TEXT_PLAIN)
        request.respond(response)

