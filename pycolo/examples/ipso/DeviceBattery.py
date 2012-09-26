# coding=utf-8
#import java.util.Timer
#import java.util.TimerTask

import random

from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap.MediaTypeRegistry import MediaTypeRegistry
from pycolo.endpoint import LocalResource


class DeviceBattery(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    power = 3.6

    def __init__(self):
        """ generated source for method __init__ """
        super(DeviceBattery, self).__init__("dev/bat")
        self.setTitle("Battery")
        self.setResourceType("ipso:dev-bat")
        #  second rt not supported by current SensiNode RD demo
        # setResourceType("ucum:V");
        self.setInterfaceDescription("core#s")
        self.isObservable(True)
        #  Set timer task scheduling
        timer = Timer()
        timer.schedule(TimeTask(), 0, 1000)

    class TimeTask(TimerTask):
        """ generated source for class TimeTask """
        def run(self):
            """ generated source for method run """
            self.power -= 0.001 * random.SystemRandom()
            #  Call changed to notify subscribers
            changed()

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, Double.toString(Math.round(self.power * 1000) / 1000), MediaTypeRegistry.TEXT_PLAIN)
