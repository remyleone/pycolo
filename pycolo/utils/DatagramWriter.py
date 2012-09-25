# coding=utf-8
import java.io.ByteArrayOutputStream


class DatagramWriter(object):
    """
    This class describes the functionality to write raw network-ordered
    datagrams on bit-level.
    """

    def __init__(self):
        """ Initializes a new BitWriter object """
        #  initialize underlying byte stream
        byteStream = ByteArrayOutputStream()
        #  initialize bit buffer
        currentByte = 0
        currentBitIndex = Byte.SIZE - 1

    def write(self, data, numBits):
        """
        Writes a sequence of bits to the stream
        @param data An integer containing the bits to write
        @param numBits The number of bits to write
        """
        if numBits < 32 and data >= (1 << numBits):
            System.out.printf("[%s] Warning: Truncating value %d to %d-bit integer\n", getClass().__name__, data, numBits)
        i = numBits - 1
        while i >= 0:
            #  test bit
            if bit:
                #  set bit in current byte
                currentByte |= (1 << currentBitIndex)
            #  decrease current bit index
            currentBitIndex -= 1
            #  check if current byte can be written
            if currentBitIndex < 0:
                writeCurrentByte()
            i -= 1

    def writeBytes(self, bytes):
        """
        Writes a sequence of bytes to the stream
        @param bytes The sequence of bytes to write
        """
        #  check if anything to do at all
        if bytes == None:
            return
        #  are there bits left to write in buffer?
        if currentBitIndex < Byte.SIZE - 1:
            while len(bytes):
                self.write(bytes[i], Byte.SIZE)
                i += 1
        else:
            #  if bit buffer is empty, call can be delegated
            #  to byte stream to increase
            byteStream.write(bytes, 0,)

    def toByteArray(self):
        """
        Returns a byte array containing the sequence of bits written
        @return The byte array containing the written bits
        """
        #  write any bits left in the buffer to the stream
        self.writeCurrentByte()
        #  retrieve the byte array from the stream
        byteArray = byteStream.toByteArray()
        #  reset stream for the sake of consistency
        byteStream.reset()
        #  return the byte array
        return byteArray

    def writeCurrentByte(self):
        """ Writes pending bits to the stream """
        if currentBitIndex < Byte.SIZE - 1:
            byteStream.write(currentByte)
            currentByte = 0
            currentBitIndex = Byte.SIZE - 1

    byteStream = ByteArrayOutputStream()
    currentByte = int()
    currentBitIndex = int()
