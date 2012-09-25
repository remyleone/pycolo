# coding=utf-8
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.SocketException
import java.util.Arrays

import thread

from pycolo.coap import EndpointAddress
from pycolo.coap import Message
from pycolo.coap import Properties
from pycolo.layers import Layer
from pycolo.utils import Datagram

#  * The class UDPLayer exchanges CoAP messages with remote endpoints using UDP
#  * datagrams. It is an unreliable channel and thus datagrams may arrive out of
#  * order, appear duplicated, or are lost without any notice, especially on lossy
#  * physical layers.
#  * <p>
#  * The UDPLayer is the base layer of the stack, sub-calssing {@link Layer}. Any
#  * {@link UpperLayer} can be stacked on top, using a {@link ch.ethz.inf.vs.californium.coap.Communicator} as
#  * stack builder.
#  * 
#  * @author Dominique Im Obersteg, Daniel Pauli, and Matthias Kovatsch


class UDPLayer(Layer):
    """ generated source for class UDPLayer """
    #  Members ////////////////////////////////////////////////////////////////
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
                    logging.severe("Could not receive datagram: " + e.getMessage())
                    e.printStackTrace()
                    continue 
                #  TODO: Dispatch to worker thread
                datagramReceived(datagram)

    #  Constructors ////////////////////////////////////////////////////////////////
    # 
    # 	 * Constructor for a new UDP layer
    # 	 * 
    # 	 * @param port The local UDP port to listen for incoming messages
    # 	 * @param daemon True if receiver thread should terminate with main thread
    #
    @overloaded
    def __init__(self, port, daemon):
        """ generated source for method __init__ """
        super(UDPLayer, self).__init__()
        #  initialize members
        self.socket = DatagramSocket(port)
        self.receiverThread = self.ReceiverThread()
        #  decide if receiver thread terminates with main thread
        self.receiverThread.setDaemon(daemon)
        #  start listening right from the beginning
        self.receiverThread.start()

    # 
    # 	 * Constructor for a new UDP layer
    # 	 
    @__init__.register(object)
    def __init___0(self):
        """ generated source for method __init___0 """
        super(UDPLayer, self).__init__()
        self.__init__(0, True)
        #  use any available port on the local host machine

    #  Commands ///////////////////////////////////////////////////////////////
    #
    # 	 * Decides if the listener thread persists after the main thread terminates
    # 	 *
    # 	 * @param on True if the listener thread should stay alive after the main
    # 	 * thread terminates. This is useful for e.g. server applications
    # 	 
    def setDaemon(self, on):
        """ generated source for method setDaemon """
        self.receiverThread.setDaemon(on)

    #  I/O implementation /////////////////////////////////////////////////////
    def doSendMessage(self, msg):
        """ generated source for method doSendMessage """
        #  retrieve payload
        payload = msg.toByteArray()
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
            if msg != None:
                #  remember when this message was received
                msg.setTimestamp(timestamp)
                msg.setPeerAddress(EndpointAddress(datagram.getAddress(), datagram.getPort()))
                if datagram.getLength() > Properties.std.getInt("RX_BUFFER_SIZE"):
                    LOG.info("Marking large datagram for blockwise transfer: {:s}".format(msg.key()))
                    msg.requiresBlockwise(True)
                #  protect against unknown exceptions
                try:
                    #  call receive handler
                    receiveMessage(msg)
                except Exception as e:
                    builder.append("Crash: ")
                    builder.append(e.getMessage())
                    builder.append('\n')
                    builder.append("                    ")
                    builder.append("Stacktrace for ")
                    builder.append(e.__class__.__name__)
                    builder.append(":\n")
                    for elem in e.getStackTrace():
                        builder.append("                    ")
                        builder.append(elem.getClassName())
                        builder.append('.')
                        builder.append(elem.getMethodName())
                        builder.append('(')
                        builder.append(elem.getFileName())
                        builder.append(':')
                        builder.append(elem.getLineNumber())
                        builder.append(")\n")
                    LOG.severe(builder.__str__())
            else:
                LOG.severe("Illeagal datagram received:\n" + data.__str__())
        else:
            LOG.info("Dropped empty datagram from: {:s}:{:d}".format(datagram.getAddress().getHostName(), datagram.getPort()))

    #  Queries /////////////////////////////////////////////////////////////////////
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
        stats = StringBuilder()
        stats.append("UDP port: ")
        stats.append(self.getPort())
        stats.append('\n')
        stats.append("Messages sent:     ")
        stats.append(numMessagesSent)
        stats.append('\n')
        stats.append("Messages received: ")
        stats.append(numMessagesReceived)
        return stats.__str__()
