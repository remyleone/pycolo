# coding=utf-8


class DatagramReader(object):
    """
    This class describes the functionality to read raw
    network-ordered datagrams on bit-level.
    """

    def __init__(self, byteArray):
        """ initialize underlying byte stream """

        self.byteStream = self.ByteArrayInputStream(byteArray)
        #  initialize bit buffer
        self.currentByte = 0
        self.currentBitIndex = -1
        #  indicates that no byte read yet

    def read(self, numBits):
        """
        Reads a sequence of bits from the stream
        @param numBits The number of bits to read
        @return An integer containing the bits read
        """
        bits = 0
        #  initialize all bits to zero
        i = numBits - 1
        while i >= 0:
            #  check whether new byte needs to be read
            if self.currentBitIndex < 0:
                self.readCurrentByte()
            #  test current bit
            if self.bit:
                #  set bit at i-th position
                bits |= (1 << i)
            #  decrease current bit index
            self.currentBitIndex -= 1
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
            count = self.byteStream.available()
        #  allocate byte array
        self.bytes = [count]
        #  are there bits left to read in buffer?
        if self.currentBitIndex >= 0:
            while i < count:
                bytes[i] = int(self.read(Byte.SIZE))
                i += 1
        else:
            #  if bit buffer is empty, call can be delegated
            #  to byte stream to increase performance
            self.byteStream.read(bytes, 0,)
        return bytes

    def readBytesLeft(self):
        """ Reads the complete sequence of bytes left in the stream """
        return self.readBytes(-1)

    def readCurrentByte(self):
        """ Reads new bits from the stream """
        #  try to read from byte stream
        val = self.byteStream.read()
        if val >= 0:
            #  byte successfully read
            self.currentByte = int(val)
        else:
            #  end of stream reached;
            #  return implicit zero bytes
            self.currentByte = 0
        #  reset current bit index
        self.currentBitIndex = Byte.SIZE - 1

    byteStream = ByteArrayInputStream()
    currentByte = int()
    currentBitIndex = int()
