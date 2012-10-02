# coding=utf-8

from pycolo.coap import MessageReceiver


class Layer(MessageReceiver):
    """
    An abstract Layer class that enforced a uniform interface for building
    a layered communications stack.
    """
    receivers = list()
    numMessagesSent = 0
    numMessagesReceived = 0

    def sendMessage(self, msg):
        """ generated source for method sendMessage """
        if msg:
            self.doSendMessage(msg)
            self.numMessagesSent += 1

    def receiveMessage(self, msg):
        """ generated source for method receiveMessage """
        if msg:
            self.numMessagesReceived += 1
            self.doReceiveMessage(msg)

    def doSendMessage(self, msg):
        pass

    def doReceiveMessage(self, msg):
        pass

    def deliverMessage(self, msg):
        #  pass message to registered receivers
        if self.receivers:
            for receiver in self.receivers:
                receiver.receiveMessage(msg)

    def registerReceiver(self, receiver):
        #  check for valid receiver
        if receiver and receiver != self:
            #  lazy creation of receiver list
            if not self.receivers:
                self.receivers = []
            #  add receiver to list
            self.receivers.add(receiver)

    def unregisterReceiver(self, receiver):
        #  remove receiver from list
        if self.receivers:
            self.receivers.remove(receiver)
