# coding=utf-8
import unittest
from pycolo import Option


class OptionTest(unittest.TestCase):

    def testRawOption(self):
        """ generated source for method testRawOption """
        dataRef = "test".getBytes()
        nrRef = 1
        opt = Option(dataRef, nrRef)
        self.assertArrayEquals(dataRef, opt.getRawValue())
        self.assertEquals(opt.getLength(),)

    def testIntOption(self):
        """ generated source for method testIntOption """
        oneByteValue = 255
        #  fits in 1 Byte
        twoBytesValue = 256
        #  needs 2 Bytes
        nrRef = 1
        optOneByte = Option(oneByteValue, nrRef)
        optTwoBytes = Option(twoBytesValue, nrRef)
        self.assertEquals(1, optOneByte.getLength())
        self.assertEquals(2, optTwoBytes.getLength())
        self.assertEquals(255, optOneByte.getIntValue())
        self.assertEquals(256, optTwoBytes.getIntValue())

    def testStringOption(self):
        """ generated source for method testStringOption """
        strRef = "test"
        nrRef = 1
        opt = Option(strRef, nrRef)
        self.assertEquals(strRef, opt.getStringValue())
        self.assertEquals(opt.getLength(),)

    def testOptionNr(self):
        """ generated source for method testOptionNr """
        dataRef = "test".getBytes()
        nrRef = 1
        opt = Option(dataRef, nrRef)
        self.assertEquals(nrRef, opt.getOptionNumber())

    def equalityTest(self):
        """ generated source for method equalityTest """
        oneByteValue = 255
        #  fits in 1 Byte
        twoBytesValue = 256
        #  needs 2 Bytes
        nrRef = 1
        optOneByte = Option(oneByteValue, nrRef)
        optTwoBytes = Option(twoBytesValue, nrRef)
        optTwoBytesRef = Option(twoBytesValue, nrRef)
        self.assertTrue(optTwoBytes == optTwoBytesRef)
        self.assertFalse(optTwoBytes == optOneByte)

    @classmethod
    def getHexString(cls, b):
        """ generated source for method getHexString """
        result = ""
        i = 0
        while len(b):
            result += int().toString((b[i] & 0xff) + 0x100, 16).substring(1)
            i += 1
        return result

if __name__ == '__main__':
    unittest.main()
