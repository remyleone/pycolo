# coding=utf-8
import random
import logging
from pycolo import UpperLayer


class AdverseLayer(UpperLayer):
    """
    This class describes the functionality of a layer that drops messages
    with a given probability in order to test retransmissions between
    MessageLayer and UDPLayer etc.
    """

    def __init__(self, txPacketLossProbability, rxPacketLossProbability):
        """ generated source for method __init__ """
        super(AdverseLayer, self).__init__()
        self.txPacketLossProbability = txPacketLossProbability
        self.rxPacketLossProbability = rxPacketLossProbability

    def __init___0(self):
        """ generated source for method __init___0 """
        super(AdverseLayer, self).__init__()
        self.__init__(0.01, 0.00)

    def doSendMessage(self, msg):
        """ generated source for method doSendMessage """
        if random.SystemRandom() >= self.txPacketLossProbability:
            self.sendMessageOverLowerLayer(msg)
        else:
            logging.info("[%s] Outgoing message dropped: %s\n" % self.getClass().__name__, msg.key())

    def doReceiveMessage(self, msg):
        """ generated source for method doReceiveMessage """
        if random.SystemRandom() >= self.rxPacketLossProbability:
            self.deliverMessage(msg)
        else:
            logging.info("[%s] Incoming message dropped: %s\n", self.getClass().__name__, msg.key())

    txPacketLossProbability = float()
    rxPacketLossProbability = float()
