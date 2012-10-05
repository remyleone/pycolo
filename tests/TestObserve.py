# coding=utf-8

#import java.text.DateFormat
#import java.text.SimpleDateFormat
#import java.util.Date
#import java.util.Timer
#import java.util.TimerTask
from pycolo import Response, codes, LocalResource

from pycolo.coap import MediaTypeRegistry


class Observe(LocalResource):
    """
    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.
    """
    #  The current time represented as string
    time = str()

    def __init__(self):
        """ Constructor for a new TimeResource """
        super(Observe, self).__init__("obs")
        self.setTitle("Observable resource which changes every 5 seconds")
        self.setResourceType("observe")
        self.isObservable(True)
        #  Set timer task scheduling
        timer = Timer()
        timer.schedule(TimeTask(), 0, 5000)

    class TimeTask(TimerTask):
        """ Defines a new timer task to return the current time """
        def run(self):
            """ generated source for method run """
            self.time = getTime()
            #  Call changed to notify subscribers
            changed()

    def getTime(self):
        """ Returns the current time """
        dateFormat = SimpleDateFormat("HH:mm:ss")
        time = Date()
        return dateFormat.format(time)

    def performGET(self, request):
        """ generated source for method performGET """
        #  create response
        response = Response(codes.RESP_CONTENT)
        #  set payload
        response.setPayload(self.time)
        response.setContentType(MediaTypeRegistry.TEXT_PLAIN)
        response.setMaxAge(5)
        #  complete the request
        request.respond(response)
