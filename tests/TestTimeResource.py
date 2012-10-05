# coding=utf-8

from pycolo.Resource import Resource
from pycolo.codes import mediaCodes, codes
import time


class TimeResource(Resource):
    """
    Defines a resource that returns the current time on a GET request.
    It also Supports observing.
    """

    #  The current time represented as string
    time = str()

    def __init__(self):
        """ generated source for method __init__ """
        super(TimeResource, self).__init__("timeResource")
        self.title = "GET the current time"
        self.resourceType = "CurrentTime"
        self.isObservable = True
        #  Set timer task scheduling
        timer = Timer()
        timer.schedule(TimeTask(), 0, 2000)

    class TimeTask(TimerTask):
        """
        Defines a new timer task to return the current time
        """
        def run(self):
            """ generated source for method run """
            self.time = self.getTime()
            #  Call changed to notify subscribers
            self.changed()

    def getTime(self):
        """ generated source for method getTime """
        return time.localtime()

    def performGET(self, request):
        """ generated source for method performGET """
        request.respond(codes.RESP_CONTENT, self.time, mediaCodes.txt)

