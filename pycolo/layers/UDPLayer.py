# coding=utf-8
import logging
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.SocketException
import java.util.Arrays

import thread

from pycolo.coap import EndpointAddress
from pycolo.layers import Layer
from pycolo.utils import Datagram


class UDPLayer(Layer):
    """
    The class UDPLayer exchanges CoAP messages with remote endpoints using UDP
    datagrams. It is an unreliable channel and thus datagrams may arrive out of
    order, appear duplicated, or are lost without any notice, especially on
    lossy physical layers.

    The UDPLayer is the base layer of the stack, sub-calssing {@link Layer}.
    Any {@link UpperLayer} can be stacked on top, using a Communicator as
    stack builder.
    """
    #  The UDP socket used to send and receive datagrams
    #  TODO Use MulticastSocket
    socket = DatagramSocket()

    #  The thread that listens on the socket for incoming datagrams
    receiverThread = ReceiverThread()

    #  Inner Classes //////////////////////////////////////////////////////////
    class ReceiverThread(Thread):
        """ generated source for class ReceiverThread """
        def __init__(self):
            """ generated source for method __init__ """
            super(ReceiverThread, self).__init__("ReceiverThread")

        def run(self):
            """ generated source for method run """
            #  always listen for incoming datagrams
            while True:
                #  allocate buffer
                #  +1 to check for > RX_BUFFER_SIZE
                #  initialize new datagram
                #  receive datagram
                try:
                    self.socket.receive(datagram)
                except IOException as e:
                    logging.critical("Could not receive datagram: " + e.getMessage())
                    continue
                #  TODO: Dispatch to worker thread
                self.datagramReceived(self.datagram)

    @overloaded
    def __init__(self, port, daemon):
        """
        Constructor for a new UDP layer
        @param port The local UDP port to listen for incoming messages
        @param daemon True if receiver thread should terminate with main thread
        """
        super(UDPLayer, self).__init__()
        #  initialize members
        self.socket = DatagramSocket(port)
        self.receiverThread = self.ReceiverThread()
        #  decide if receiver thread terminates with main thread
        self.receiverThread.setDaemon(daemon)
        #  start listening right from the beginning
        self.receiverThread.start()

    def __init___0(self):
        """ Constructor for a new UDP layer """
        super(UDPLayer, self).__init__()
        self.__init__(0, True)
        #  use any available port on the local host machine

    def setDaemon(self, on):
        """
        Decides if the listener thread persists after the main thread
        terminates
        @param on True if the listener thread should stay alive after the main
        thread terminates. This is useful for e.g. server applications
        """
        self.receiverThread.setDaemon(on)

    def doSendMessage(self, msg):
        payload = msg.toByteArray()  # retrieve payload
        #  create datagram
        datagram = DatagramPacket(payload, msg.getPeerAddress().getAddress(), msg.getPeerAddress().getPort(),)
        #  remember when this message was sent for the first time
        #  set timestamp only once in order
        #  to handle retransmissions correctly
        if msg.getTimestamp() == -1:
            msg.setTimestamp(System.nanoTime())
        #  send it over the UDP socket
        self.socket.send(datagram)

    def doReceiveMessage(self, msg):
        """ generated source for method doReceiveMessage """
        #  pass message to registered receivers
        self.deliverMessage(msg)

    #  Internal ///////////////////////////////////////////////////////////////
    def datagramReceived(self, datagram):
        """ generated source for method datagramReceived """
        if datagram.getLength() > 0:
            #  get current time
            #  extract message data from datagram
            #  create new message from the received data
            if self.msg != None:
                #  remember when this message was received
                self.msg.setTimestamp(timestamp)
                self.msg.setPeerAddress(EndpointAddress(datagram.getAddress(), datagram.getPort()))
                if datagram.getLength() > Properties.std.getInt("RX_BUFFER_SIZE"):
                    logging.info("Marking large datagram for blockwise transfer: {:s}".format(msg.key()))
                    self.msg.requiresBlockwise(True)
                #  protect against unknown exceptions
                try:
                    #  call receive handler
                    receiveMessage(msg)
                except Exception as e:
                    self.builder.append("Crash: ")
                    self.builder.append(e.getMessage())
                    self.builder.append('\n')
                    self.builder.append("                    ")
                    self.builder.append("Stacktrace for ")
                    self.builder.append(e.__class__.__name__)
                    self.builder.append(":\n")
                    for elem in e.getStackTrace():
                        self.builder.append("                    ")
                        self.builder.append(elem.getClassName())
                        self.builder.append('.')
                        self.builder.append(elem.getMethodName())
                        self.builder.append('(')
                        self.builder.append(elem.getFileName())
                        self.builder.append(':')
                        self.builder.append(elem.getLineNumber())
                        self.builder.append(")\n")
                    logging.critical(self.builder.__str__())
            else:
                logging.critical("Illeagal datagram received:\n" + data.__str__())
        else:
            logging.info("Dropped empty datagram from: {:s}:{:d}".format(datagram.getAddress().getHostName(), datagram.getPort()))

    #  Queries ////////////////////////////////////////////////////////////////
    #
    # 	 * Checks whether the listener thread persists after the main thread
    # 	 * terminates
    # 	 *
    # 	 * @return True if the listener thread stays alive after the main thread
    # 	 * terminates. This is useful for e.g. server applications
    #
    def isDaemon(self):
        """ generated source for method isDaemon """
        return self.receiverThread.isDaemon()

    def getPort(self):
        """ generated source for method getPort """
        return self.socket.getLocalPort()

    def getStats(self):
        """ generated source for method getStats """
        stats = dict()
        stats["UDP port"] = self.port
        stats["Messages sent"] = self.numMessagesSent
        stats["Messages received"] = self.numMessagesReceived
        return str(stats)
