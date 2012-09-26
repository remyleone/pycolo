# coding=utf-8
#import java.util.Timer
#import java.util.TimerTask

import random

from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap.MediaTypeRegistry import MediaTypeRegistry
from pycolo.endpoint import LocalResource


class PowerCumulative(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    power = 0

    def __init__(self):
        """ generated source for method __init__ """
        super(PowerCumulative, self).__init__("pwr/kwh")
        self.setTitle("Cumulative Power")
        self.setResourceType("ipso:pwr-kwh")
        #  second rt not supported by current SensiNode RD demo
        # setResourceType("ucum:kWh");
        self.setInterfaceDescription("core#s")
        self.isObservable(True)
        #  Set timer task scheduling
        timer = Timer()
        timer.schedule(TimeTask(), 0, 1000)

    class TimeTask(TimerTask):
        """ generated source for class TimeTask """
        def run(self):
            """ generated source for method run """
            if PowerRelay.getRelay():
                self.power += Math.round(10 * random.SystemRandom() * (PowerDimmer.getDimmer() / 100))
                #  Call changed to notify subscribers
                changed()

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, Double.toString(self.power), MediaTypeRegistry.TEXT_PLAIN)
