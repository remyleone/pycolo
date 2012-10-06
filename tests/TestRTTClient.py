# coding=utf-8
import logging

import unittest
import sys

class RTTClient:
    """
    "Usage: " + RTTClient.__class__.getSimpleName() + " URI"
    """
    uriString = ""
    n = 1000
    sent = 0
    received = 0
    total = 0
    max = 0

    def main(self, cls, args):
        """ Main method of this client.
        :param args:
        :param cls:
        """
        if args:
            #  input URI from command line arguments
            try:
                uri = URI(args[0])
                cls.uriString = args[0]
            except URISyntaxException as e:
                logging.critical("Invalid URI: " + e.getMessage())
                sys.exit(-1)
            if len(args):
                try:
                    cls.n = int(args[1])
                except NumberFormatException as e:
                    logging.critical("Invalid number: " + e.getMessage())
                    sys.exit(-1)
            Runtime.getRuntime().addShutdownHook(Thread())
            while i < cls.n:
                request.enableResponseQueue(True)
                request.setURI(uri)
                try:
                    request.execute()
                except IOException as e:
                    #  TODO Auto-generated catch block
                    e.printStackTrace()
                    sys.exit(-1)
                try:
                    cls.sent += 1
                    if response:
                        cls.received += 1
                        if response.getRTT() > cls.max:
                            cls.max = response.getRTT()
                        if response.getRTT() < cls.min:
                            cls.min = response.getRTT()
                        if response.getRTT() < 0:
                            logging.info("ERROR: Response untimed, time=" + response.getRTT())
                        elif request.getRetransmissioned() > 0:
                            logging.info("WARNING: Response after retransmission, time=" + response.getRTT())
                        else:
                            logging.info("time=" + response.getRTT() + "ms")
                        cls.total += response.getRTT()
                    else:
                        logging.info"No response received"
                except InterruptedException as e:
                    #  TODO Auto-generated catch block
                    e.printStackTrace()
                i += 1

if __name__ == '__main__':
    unittest.main()
