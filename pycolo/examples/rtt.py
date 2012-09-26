# coding=utf-8
import java.net.URI
import java.net.URISyntaxException

import logging


class RTTClient(object):
    """ generated source for class RTTClient """
    uriString = ""
    n = 1000
    sent = 0
    received = 0
    total = 0
    min = int().MAX_VALUE
    max = 0

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        uri = None
        Log.setLevel(Level.WARNING)
        Log.init()
        if len(args):
            #  input URI from command line arguments
            try:
                uri = URI(args[0])
                cls.uriString = args[0]
            except URISyntaxException as e:
                System.err.println("Invalid URI: " + e.getMessage())
                System.exit(-1)
            if len(args):
                try:
                    cls.n = Integer.parseInt(args[1])
                except NumberFormatException as e:
                    System.err.println("Invalid number: " + e.getMessage())
                    System.exit(-1)
            Runtime.getRuntime().addShutdownHook(Thread())
            while i < cls.n:
                request.enableResponseQueue(True)
                request.setURI(uri)
                try:
                    request.execute()
                except IOException as e:
                    #  TODO Auto-generated catch block
                    e.printStackTrace()
                    System.exit(-1)
                try:
                    cls.sent += 1
                    if response != None:
                        cls.received += 1
                        if response.getRTT() > cls.max:
                            cls.max = response.getRTT()
                        if response.getRTT() < cls.min:
                            cls.min = response.getRTT()
                        if response.getRTT() < 0:
                            print "ERROR: Response untimed, time=" + response.getRTT()
                        elif request.getRetransmissioned() > 0:
                            print "WARNING: Response after retransmission, time=" + response.getRTT()
                        else:
                            print "time=" + response.getRTT() + "ms"
                        cls.total += response.getRTT()
                    else:
                        print
                        var = "No response received"
                except InterruptedException as e:
                    #  TODO Auto-generated catch block
                    e.printStackTrace()
                i += 1
        else:
            #  display help
            print
            var = "Californium (Cf) RTT Client"
            print
            var = "(c) 2012, Institute for Pervasive Computing, ETH Zurich"
            print 
            print
            var = "Usage: " + RTTClient.__class__.getSimpleName() + " URI"
            print
            var = "  URI: The CoAP URI of the remote resource to measure"


if __name__ == '__main__':
    import sys
    RTTClient.main(sys.argv)
