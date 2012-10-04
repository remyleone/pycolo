# coding=utf-8

import logging
import json
from pycolo import Response
from pycolo import codes
from pycolo import Resource
from pycolo.codes import mediaCodes

class ParisWeatherResource(Resource):
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
        self.supported.add(mediaCodes.text)
        self.supported.add(mediaCodes.json)
        for ct in supported:
            self.setContentTypeCode(ct)
        self.getParisWeather()
        #  Set timer task scheduling
        timer = Timer()
        timer.schedule(ZurichWeatherTask(), 0, self.WEATHER_MAX_AGE)

    class ParisWeatherTask(TimerTask):

        def run(self):
            """ generated source for method run """
            weatherOLD = str(self.weatherXML)
            self.getParisWeather()
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

    def performGET(self, request):
        """ generated source for method performGET """
        ct = MediaTypeRegistry.TEXT_PLAIN
        if (ct=MediaTypeRegistry.contentNegotiation(ct, self.supported, request.getOptions(OptionNumberRegistry.ACCEPT))) == MediaTypeRegistry.UNDEFINED:
            request.respond(codes.RESP_NOT_ACCEPTABLE, "Supports text/plain and application/xml")
            return
        response = Response(codes.RESP_CONTENT)
        response.setMaxAge(self.WEATHER_MAX_AGE / 1000)
        if ct == MediaTypeRegistry.APPLICATION_XML:
            response.setPayload(self.weatherXML, MediaTypeRegistry.APPLICATION_XML)
        else:
            response.setPayload(self.weatherPLAIN, MediaTypeRegistry.TEXT_PLAIN)
        request.respond(response)