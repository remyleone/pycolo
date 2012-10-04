# coding=utf-8

import logging
from pycolo import Layer


class UpperLayer(Layer):
    """ generated source for class UpperLayer """
    def sendMessageOverLowerLayer(self, msg):
        """ generated source for method sendMessageOverLowerLayer """
        #  check if lower layer assigned
        if self.lowerLayer is not None:
            self.lowerLayer.sendMessage(msg)
        else:
            logging.critical("[%s] ERROR: No lower layer present", self.getClass().__name__)

    def setLowerLayer(self, layer):
        """ generated source for method setLowerLayer """
        #  unsubscribe from old lower layer
        if self.lowerLayer is not None:
            self.lowerLayer.unregisterReceiver(self)
        #  set new lower layer
        lowerLayer = layer
        #  subscribe to new lower layer
        if lowerLayer != None:
            lowerLayer.registerReceiver(self)

    def getLowerLayer(self):
        """ generated source for method getLowerLayer """
        return self.lowerLayer

    lowerLayer = Layer()
