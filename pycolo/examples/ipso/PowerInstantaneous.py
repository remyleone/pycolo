# coding=utf-8

#import java.util.Timer
#import java.util.TimerTask
import math
import random

from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo import mediaTypeRegistry
from pycolo.endpoint import LocalResource


class PowerInstantaneous(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    power = 0

    def __init__(self):
        """ generated source for method __init__ """
        super(PowerInstantaneous, self).__init__("pwr/w")
        self.title = "Instantaneous Power"
        self.setResourceType("ipso:pwr-w")
        #  second rt not supported by current SensiNode RD demo
        # setResourceType("ucum:W");
        self.setInterfaceDescription("core#s")
        self.isObservable(True)
        #  Set timer task scheduling
        timer = Timer()
        timer.schedule(TimeTask(), 0, 1000)

    class TimeTask(TimerTask):
        """ generated source for class TimeTask """
        def run(self):
            """ generated source for method run """
            if self.PowerRelay.getRelay():
                self.power = 1500 * random.SystemRandom() * (PowerDimmer.getDimmer() / 100)
            else:
                #  skip changed() update if nothing changed
                if self.power == 0:
                    return
                self.power = 0
            #  Call changed to notify subscribers
            self.changed()

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, \
                        str(self.power), \
                        mediaTypeRegistry["TEXT_PLAIN"])
