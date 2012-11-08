# coding=utf-8
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
        def run(self):
            pass

        #            """ generated source for method run """
        #            weatherOLD = str(self.weatherXML)
        #            self.getParisWeather()
        #            if not weatherOLD == self.weatherXML:
        #                changed()

        def getParisWeather(self):
        #        conn = http.client.HTTPConnection("http://openweathermap.org")
        #        conn.request("GET", "/data/2.1/find/city?lat=48.8566140&lon=2.3522219&cnt=1")
        #        weather = conn.getresponse()
        #        if conn.getresponse() == 200:
        #            print(weather.read())
            pass

        def performGET(self, request):
            """ generated source for method performGET
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
