# coding=utf-8

"""
TODO
"""

from pycolo.resource import Resource

class ParisWeatherResource(Resource):
    """
    Defines a resource that returns the current weather on a GET request.
    """

    def __init__(self):
        """
        Constructor for a new ParisWeatherResource
        """

    #        super(ZurichWeatherResource, self).__init__("weatherResource")
    #        self.title = "GET the current weather in Paris"
    #        self.setResourceType("ZurichWeather")
    #        self.observable = True
    #        self.supported.add(mediaCodes.text)
    #        self.supported.add(mediaCodes.json)
    #        for ct in supported:
    #            self.setContentTypeCode(ct)
    #        self.getParisWeather()
    #        #  Set timer task scheduling
    #        timer = Timer()
    #        timer.schedule(ParisWeatherTask(), 0, self.WEATHER_MAX_AGE)

    class ParisWeatherTask:
        """
        TODO
        """

        def run(self):
            """
            TODO
            """
            pass

        #            weatherOLD = str(self.weatherXML)
        #            self.getParisWeather()
        #            if not weatherOLD == self.weatherXML:
        #                changed()

        def getParisWeather(self):
            """
            TODO
            """
            pass

        def performGET(self, request):
            """
            TODO
            :param request:
            """
            #        ct = mediaCodes.text
            #        if ct=MediaTypeRegistry.contentNegotiation(ct, self.supported, request.getOptions(OptionNumberRegistry.ACCEPT)) == MediaTypeRegistry.UNDEFINED:
            #        request.respond(codes.RESP_NOT_ACCEPTABLE, "Supports text/plain and application/xml")
            #        return
            #    response = Response(codes.RESP_CONTENT)
            #    response.setMaxAge(self.WEATHER_MAX_AGE / 1000)
            #    if ct == MediaTypeRegistry.APPLICATION_XML:
            #        response.payload = self.weatherXML, mediaCodes.APPLICATION_XML
            #    else:
            #        response.payload = self.weatherPLAIN, mediaCodes.text
            #    request.respond(response)
            #
