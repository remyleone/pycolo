# coding=utf-8
import random
from pycolo.coap import Message
from pycolo.layers import UpperLayer


class AdverseLayer(UpperLayer):
    """
    This class describes the functionality of a layer that drops messages
    with a given probability in order to test retransmissions between
    MessageLayer and UDPLayer etc.
    """
    @overloaded
    def __init__(self, txPacketLossProbability, rxPacketLossProbability):
        """ generated source for method __init__ """
        super(AdverseLayer, self).__init__()
        self.txPacketLossProbability = txPacketLossProbability
        self.rxPacketLossProbability = rxPacketLossProbability

    @__init__.register(object)
    def __init___0(self):
        """ generated source for method __init___0 """
        super(AdverseLayer, self).__init__()
        self.__init__(0.01, 0.00)

    def doSendMessage(self, msg):
        """ generated source for method doSendMessage """
        if random.SystemRandom() >= txPacketLossProbability:
            sendMessageOverLowerLayer(msg)
        else:
            System.err.printf("[%s] Outgoing message dropped: %s\n", getClass().__name__, msg.key())

    def doReceiveMessage(self, msg):
        """ generated source for method doReceiveMessage """
        if random.SystemRandom() >= rxPacketLossProbability:
            deliverMessage(msg)
        else:
            System.err.printf("[%s] Incoming message dropped: %s\n", getClass().__name__, msg.key())

    txPacketLossProbability = float()
    rxPacketLossProbability = float()
