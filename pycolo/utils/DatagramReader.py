# coding=utf-8
import java.io.ByteArrayInputStream


class DatagramReader(object):
    """
    This class describes the functionality to read raw
    network-ordered datagrams on bit-level.
    """
    #  Constructors ///////////////////////////////////////////////////////////
    #
    # 	 * Initializes a new BitReader object
    # 	 * 
    # 	 * @param byteArray The byte array to read from
    # 	 
    def __init__(self, byteArray):
        """ generated source for method __init__ """
        #  initialize underlying byte stream
        byteStream = ByteArrayInputStream(byteArray)
        #  initialize bit buffer
        currentByte = 0
        currentBitIndex = -1
        #  indicates that no byte read yet

    #  Methods ////////////////////////////////////////////////////////////////
    #
    # 	 * Reads a sequence of bits from the stream
    # 	 *
    # 	 * @param numBits The number of bits to read
    # 	 *
    # 	 * @return An integer containing the bits read
    #
    def read(self, numBits):
        """ generated source for method read """
        bits = 0
        #  initialize all bits to zero
        i = numBits - 1
        while i >= 0:
            #  check whether new byte needs to be read
            if currentBitIndex < 0:
                readCurrentByte()
            #  test current bit
            if bit:
                #  set bit at i-th position
                bits |= (1 << i)
            #  decrease current bit index
            currentBitIndex -= 1
            i -= 1
        return bits

    def readBytes(self, count):
        """
        Reads a sequence of bytes from the stream
        @param count The number of bytes to read
        @return The sequence of bytes read from the stream
        """
        #  for negative count values, read all bytes left
        if count < 0:
            count = byteStream.available()
        #  allocate byte array
        bytes = [count]
        #  are there bits left to read in buffer?
        if currentBitIndex >= 0:
            while i < count:
                bytes[i] = int(self.read(Byte.SIZE))
                i += 1
        else:
            #  if bit buffer is empty, call can be delegated
            #  to byte stream to increase performance
            byteStream.read(bytes, 0,)
        return bytes

    def readBytesLeft(self):
        """ Reads the complete sequence of bytes left in the stream """
        return self.readBytes(-1)

    def readCurrentByte(self):
        """ Reads new bits from the stream """
        #  try to read from byte stream
        val = byteStream.read()
        if val >= 0:
            #  byte successfully read
            currentByte = int(val)
        else:
            #  end of stream reached;
            #  return implicit zero bytes
            currentByte = 0
        #  reset current bit index
        currentBitIndex = Byte.SIZE - 1

    #  Attributes //////////////////////////////////////////////////////////////
    byteStream = ByteArrayInputStream()
    currentByte = int()
    currentBitIndex = int()
