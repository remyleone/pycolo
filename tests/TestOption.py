# coding=utf-8

"""
Testing suite for Option management inside messages.
"""

import unittest
import math
from pycolo.endpoint import Endpoint

def getLength(obj):
    """
    This method returns the bit-length of the argument

    :param obj: Argument we want the bit-length of
    """
    if isinstance(obj, int):
        return math.ceil(obj.bit_length() / 8)
    if isinstance(obj, str):
        len(bytearray(obj, "utf-8"))

class OptionTest(unittest.TestCase):
    """
    Test options.
    """

    def testRawOption(self):
        """
        TODO
        """
        dataRef = b"test"
        nrRef = 1
        options = {nrRef: dataRef}
        self.assertEquals(dataRef, options[nrRef])
        self.assertEquals(len(options), 1)

    def testIntOption(self):
        """
        TODO
        """
        oneByteValue = 255  # fits in 1 Byte
        twoBytesValue = 256  # needs 2 Bytes
        nrRef = 1
        optOneByte = {nrRef: oneByteValue}
        optTwoBytes = {nrRef: twoBytesValue}
        self.assertEquals(1, getLength(oneByteValue))
        self.assertEquals(2, getLength(twoBytesValue))
        self.assertEquals(255, optOneByte[nrRef])
        self.assertEquals(256, optTwoBytes[nrRef])

class TestSeparate(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        res = ResourceTest()
        server = Endpoint()
        server.addResource(res)
