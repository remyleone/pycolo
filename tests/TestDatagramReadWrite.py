# coding=utf-8
#import java.nio.ByteBuffer
#import java.nio.ByteOrder
import unittest


class DatagramReadWriteTest(unittest.TestCase):
    """
    This unit test examines the DatagramReader and DatagramWriter
    classes for consistency and correct data format.
    """
    def test32BitInt(self):
        intIn = 0x87654321
        writer.write(intIn, 32)
        reader = DatagramReader(writer.toByteArray())
        intOut = reader.read(32)
        self.assertEquals(intIn, intOut)

    def test32BitIntZero(self):
        """ generated source for method test32BitIntZero """
        intIn = 0x00000000
        writer = DatagramWriter()
        writer.write(intIn, 32)
        reader = DatagramReader(writer.toByteArray())
        intOut = reader.read(32)
        self.assertEquals(intIn, intOut)

    def test32BitIntOne(self):
        """ generated source for method test32BitIntOne """
        intIn = 0xFFFFFFFF
        writer = DatagramWriter()
        writer.write(intIn, 32)
        reader = DatagramReader(writer.toByteArray())
        intOut = reader.read(32)
        self.assertEquals(intIn, intOut)

    def test16BitInt(self):
        """ generated source for method test16BitInt """
        intIn = 0x00004321
        writer = DatagramWriter()
        writer.write(intIn, 16)
        reader = DatagramReader(writer.toByteArray())
        intOut = reader.read(16)
        self.assertEquals(intIn, intOut)

    def test8BitInt(self):
        """ generated source for method test8BitInt """
        intIn = 0x00000021
        writer = DatagramWriter()
        writer.write(intIn, 8)
        reader = DatagramReader(writer.toByteArray())
        intOut = reader.read(8)
        self.assertEquals(intIn, intOut)

    def test4BitInt(self):
        """ generated source for method test4BitInt """
        intIn = 0x0000005
        writer = DatagramWriter()
        writer.write(intIn, 4)
        reader = DatagramReader(writer.toByteArray())
        intOut = reader.read(4)
        self.assertEquals(intIn, intOut)

    def test2BitInt(self):
        """ generated source for method test2BitInt """
        intIn = 0x00000002
        writer = DatagramWriter()
        writer.write(intIn, 2)
        reader = DatagramReader(writer.toByteArray())
        intOut = reader.read(2)
        self.assertEquals(intIn, intOut)

    def test1BitInt(self):
        """ generated source for method test1BitInt """
        intIn = 0x00000001
        writer = DatagramWriter()
        writer.write(intIn, 1)
        reader = DatagramReader(writer.toByteArray())
        intOut = reader.read(1)
        self.assertEquals(intIn, intOut)

    def testByteOrder(self):
        """ generated source for method testByteOrder """
        intIn = 1234567890
        writer = DatagramWriter()
        writer.write(intIn, 32)
        data = writer.toByteArray()
        buf = self.ByteBuffer.wrap(data)
        buf.order(self.ByteOrder.BIG_ENDIAN)
        intTrans = buf.getInt()
        self.assertEquals(intIn, intTrans)
        reader = DatagramReader(data)
        intOut = reader.read(32)
        self.assertEquals(intIn, intOut)

    def testAlignedBytes(self):
        """ generated source for method testAlignedBytes """
        bytesIn = "Some aligned Bytes".getBytes()
        writer = DatagramWriter()
        writer.writeBytes(bytesIn)
        reader = DatagramReader(writer.toByteArray())
        bytesOut = reader.readBytes()
        self.assertArrayEquals(bytesIn, bytesOut)

    def testUnalignedBytes1(self):
        """ generated source for method testUnalignedBytes1 """
        bitCount = 1
        bitsIn = 0x1
        bytesIn = "Some unaligned Bytes".getBytes()
        writer = DatagramWriter()
        writer.write(bitsIn, bitCount)
        writer.writeBytes(bytesIn)
        reader = DatagramReader(writer.toByteArray())
        bitsOut = reader.read(bitCount)
        bytesOut = reader.readBytes()
        self.assertEquals(bitsIn, bitsOut)
        self.assertArrayEquals(bytesIn, bytesOut)

    def testUnalignedBytes3(self):
        """ generated source for method testUnalignedBytes3 """
        bitCount = 3
        bitsIn = 0x5
        bytesIn = "Some unaligned Bytes".getBytes()
        writer = DatagramWriter()
        writer.write(bitsIn, bitCount)
        writer.writeBytes(bytesIn)
        reader = DatagramReader(writer.toByteArray())
        bitsOut = reader.read(bitCount)
        bytesOut = reader.readBytes()
        self.assertEquals(bitsIn, bitsOut)
        self.assertArrayEquals(bytesIn, bytesOut)

    def testUnalignedBytes7(self):
        """ generated source for method testUnalignedBytes7 """
        bitCount = 7
        bitsIn = 0x69
        bytesIn = "Some unaligned Bytes".getBytes()
        writer = DatagramWriter()
        writer.write(bitsIn, bitCount)
        writer.writeBytes(bytesIn)
        reader = DatagramReader(writer.toByteArray())
        bitsOut = reader.read(bitCount)
        bytesOut = reader.readBytes()
        self.assertEquals(bitsIn, bitsOut)
        self.assertArrayEquals(bytesIn, bytesOut)

    def testBytesLeft(self):
        """ generated source for method testBytesLeft """
        bitCount = 8
        bitsIn = 0xAA
        bytesIn = "Some payload".getBytes()
        writer = DatagramWriter()
        writer.write(bitsIn, bitCount)
        writer.writeBytes(bytesIn)
        reader = DatagramReader(writer.toByteArray())
        bitsOut = reader.read(bitCount)
        bytesOut = reader.readBytesLeft()
        self.assertEquals(bitsIn, bitsOut)
        self.assertArrayEquals(bytesIn, bytesOut)

    def testBytesLeftUnaligned(self):
        """ generated source for method testBytesLeftUnaligned """
        bitCount = 7
        bitsIn = 0x55
        bytesIn = "Some payload".getBytes()
        writer = DatagramWriter()
        writer.write(bitsIn, bitCount)
        writer.writeBytes(bytesIn)
        reader = DatagramReader(writer.toByteArray())
        bitsOut = reader.read(bitCount)
        bytesOut = reader.readBytesLeft()
        self.assertEquals(bitsIn, bitsOut)
        self.assertArrayEquals(bytesIn, bytesOut)

    def testGETRequestHeader(self):
        """ generated source for method testGETRequestHeader """
        versionIn = 1
        versionSz = 2
        typeIn = 0
        #  Confirmable
        typeSz = 2
        optionCntIn = 1
        optionCntSz = 4
        codeIn = 1
        #  GET Request
        codeSz = 8
        msgIdIn = 0x1234
        msgIdSz = 16
        writer = DatagramWriter()
        writer.write(versionIn, versionSz)
        writer.write(typeIn, typeSz)
        writer.write(optionCntIn, optionCntSz)
        writer.write(codeIn, codeSz)
        writer.write(msgIdIn, msgIdSz)
        data = writer.toByteArray()
        dataRef = [0x41, 0x01, 0x12, 0x34]
        self.assertArrayEquals(dataRef, data)
        reader = DatagramReader(data)
        versionOut = reader.read(versionSz)
        typeOut = reader.read(typeSz)
        optionCntOut = reader.read(optionCntSz)
        codeOut = reader.read(codeSz)
        msgIdOut = reader.read(msgIdSz)
        self.assertEquals(versionIn, versionOut)
        self.assertEquals(typeIn, typeOut)
        self.assertEquals(optionCntIn, optionCntOut)
        self.assertEquals(codeIn, codeOut)
        self.assertEquals(msgIdIn, msgIdOut)

if __name__ == '__main__':
    unittest.main()
