# coding=utf-8
import java.util.ArrayList

from pycolo.coap import Message
from pycolo.coap import MessageReceiver


class Layer(MessageReceiver):
    """
    An abstract Layer class that enforced a uniform interface for building
    a layered communications stack.
    """
    receivers = list()
    numMessagesSent = int()
    numMessagesReceived = int()

    def sendMessage(self, msg):
        """ generated source for method sendMessage """
        if msg != None:
            self.doSendMessage(msg)
            self.numMessagesSent += 1

    def receiveMessage(self, msg):
        """ generated source for method receiveMessage """
        if msg != None:
            self.numMessagesReceived += 1
            self.doReceiveMessage(msg)

    def doSendMessage(self, msg):
        """ generated source for method doSendMessage """

    def doReceiveMessage(self, msg):
        """ generated source for method doReceiveMessage """

    def deliverMessage(self, msg):
        """ generated source for method deliverMessage """
        #  pass message to registered receivers
        if self.receivers != None:
            for receiver in self.receivers:
                receiver.receiveMessage(msg)

    def registerReceiver(self, receiver):
        """ generated source for method registerReceiver """
        #  check for valid receiver
        if receiver != None and receiver != self:
            #  lazy creation of receiver list
            if self.receivers == None:
                self.receivers = ArrayList()
            #  add receiver to list
            self.receivers.add(receiver)

    def unregisterReceiver(self, receiver):
        """ generated source for method unregisterReceiver """
        #  remove receiver from list
        if self.receivers != None:
            self.receivers.remove(receiver)

    def getNumMessagesSent(self):
        """ generated source for method getNumMessagesSent """
        return self.numMessagesSent

    def getNumMessagesReceived(self):
        """ generated source for method getNumMessagesReceived """
        return self.numMessagesReceived
