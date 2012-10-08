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

    def __init__(self, txPacketLossProbability=0.0, rxPacketLossProbability=0.0):
        self.txPacketLossProbability = txPacketLossProbability
        self.rxPacketLossProbability = rxPacketLossProbability

    def doSendMessage(self, msg):
        if random.SystemRandom() >= self.txPacketLossProbability:
            self.sendMessageOverLowerLayer(msg)
        else:
            logging.info("[%s] Outgoing message dropped: %s\n" % self.getClass().__name__, msg.key())

    def doReceiveMessage(self, msg):
        if random.SystemRandom() >= self.rxPacketLossProbability:
            self.deliverMessage(msg)
        else:
            logging.info("[%s] Incoming message dropped: %s\n", self.getClass().__name__, msg.key())