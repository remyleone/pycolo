# coding=utf-8

import unittest
import math

class TestBytes(unittest.TestCase):

    def test32BitInt(self):
        intIn = 0x87654321
        temp = intIn.to_bytes(32, 'little')
        intOut = int.from_bytes(temp, 'little')
        self.assertEquals(intIn, intOut)

    def test32BitIntZero(self):
        intIn = int()
        temp = intIn.to_bytes(32, 'little')
        intOut = int.from_bytes(temp, 'little')
        self.assertEquals(intIn, intOut)

    def test32BitIntOne(self):
        intIn = 0xFFFFFFFF
        temp = intIn.to_bytes(32, 'little')
        intOut = int.from_bytes(temp, 'little')
        self.assertEquals(intIn, intOut)

    def test16BitInt(self):
        intIn = 0x00004321
        temp = intIn.to_bytes(16, 'little')
        intOut = int.from_bytes(temp, 'little')
        self.assertEquals(intIn, intOut)

    def test8BitInt(self):
        intIn = 0x00000021
        temp = intIn.to_bytes(8, 'little')
        intOut = int.from_bytes(temp, 'little')
        self.assertEquals(intIn, intOut)

    def test4BitInt(self):
        intIn = 0x0000005
        temp = intIn.to_bytes(4, 'little')
        intOut = int.from_bytes(temp, 'little')
        self.assertEquals(intIn, intOut)

    def test2BitInt(self):
        intIn = 0x00000002
        temp = intIn.to_bytes(2, 'little')
        intOut = int.from_bytes(temp, 'little')
        self.assertEquals(intIn, intOut)

    def test1BitInt(self):
        intIn = 0x00000001
        temp = intIn.to_bytes(1, 'little')
        intOut = int.from_bytes(temp, 'little')
        self.assertEquals(intIn, intOut)

    def testAlignedBytes(self):
        bytesIn = b"Some aligned Bytes"
        temp = int.from_bytes(bytesIn, byteorder='little')
        bytesOut = temp.to_bytes(math.ceil(temp.bit_length() / 8), byteorder='little').strip(b"\x00")
        self.assertEquals(bytesIn, bytesOut)

    def testUnalignedBytes1(self):
        bitsIn = 1
        bitCount = bitsIn.bit_length()
        bytesIn = b"Some unaligned Bytes"
        temp = bitsIn.to_bytes(math.ceil(bitCount / 8),'little') + bytesIn
        bitsOut = temp[math.ceil(bitCount / 8) - 1]
        bytesOut = temp[math.ceil(bitCount / 8):]
        self.assertEquals(bitsIn, bitsOut)
        self.assertEquals(bytesIn, bytesOut)

    def testUnalignedBytes3(self):
        bitsIn = 5
        bitCount = bitsIn.bit_length()
        bytesIn = b"Some unaligned Bytes"
        temp = bitsIn.to_bytes(math.ceil(bitCount / 8),'little') + bytesIn
        bitsOut = temp[math.ceil(bitCount / 8) - 1]
        bytesOut = temp[math.ceil(bitCount / 8):]
        self.assertEquals(bitsIn, bitsOut)
        self.assertEquals(bytesIn, bytesOut)

    def testUnalignedBytes7(self):
        bitsIn = 69
        bitCount = bitsIn.bit_length()
        bytesIn = b"Some unaligned Bytes"
        temp = bitsIn.to_bytes(math.ceil(bitCount / 8),'little') + bytesIn
        bitsOut = temp[math.ceil(bitCount / 8) - 1]
        bytesOut = temp[math.ceil(bitCount / 8):]
        self.assertEquals(bitsIn, bitsOut)
        self.assertEquals(bytesIn, bytesOut)

    def testBytesLeft(self):
        bitsIn = 0xaa
        bitCount = bitsIn.bit_length()
        bytesIn = b"Some unaligned Bytes"
        temp = bitsIn.to_bytes(math.ceil(bitCount / 8),'little') + bytesIn
        bitsOut = temp[math.ceil(bitCount / 8) - 1]
        bytesOut = temp[math.ceil(bitCount / 8):]
        self.assertEquals(bitsIn, bitsOut)
        self.assertEquals(bytesIn, bytesOut)

    def testBytesLeftUnaligned(self):
        bitsIn = 55
        bitCount = bitsIn.bit_length()
        bytesIn = b"Some unaligned Bytes"
        temp = bitsIn.to_bytes(math.ceil(bitCount / 8),'little') + bytesIn
        bitsOut = temp[math.ceil(bitCount / 8) - 1]
        bytesOut = temp[math.ceil(bitCount / 8):]
        self.assertEquals(bitsIn, bitsOut)
        self.assertEquals(bytesIn, bytesOut)


if __name__ == '__main__':
    unittest.main()
