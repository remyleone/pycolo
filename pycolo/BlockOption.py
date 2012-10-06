# coding=utf-8
import math
from pycolo import Option


class BlockOption(Option):

    def encode(cls, num, szx, m):
        value = 0
        value |= (szx & 0x7)
        value |= (1 if m else 0) << 3
        value |= num << 4
        return value

    def __init__(self, nr):
        super(BlockOption, self).__init__(nr)

    @__init__.register(object, int, int, int, bool)
    def __init___0(self, nr):
        super(BlockOption, self).__init__(nr)

    def setValue(self, num, szx, m):
        self.setIntValue(self.encode(num, szx, m))

    def getNUM(self):
        return self.getIntValue() >> 4

    def setNUM(self, num):
        self.setValue(num, self.getSZX(), self.getM())

    def getSZX(self):
        return self.getIntValue() & 0x7

    def setSZX(self, szx):
        self.setValue(self.getNUM(), szx, self.getM())

    def getSize(self):
        return self.decodeSZX(self.getIntValue() & 0x7)

    def setSize(self, size):
        self.setValue(self.getNUM(), self.encodeSZX(size), self.getM())

    def getM(self):
        return (self.getIntValue() >> 3 & 0x1) != 0

    def setM(self, m):
        self.setValue(self.getNUM(), self.getSZX(), m)

    def decodeSZX(cls, szx):
        """
        Decodes a 3-bit SZX value into a block size as specified by
        draft-IETF-core-block-03, section-2.1:
        0 --> 2^4 = 16 bytes
        ...
        6 --> 2^10 = 1024 bytes
        """
        return 1 << (szx + 4)

    def encodeSZX(cls, blockSize):
        """
        Encodes a block size into a 3-bit SZX value as specified by
        draft-ietf-core-block-03, section-2.1:
        16 bytes = 2^4 --> 0
        ...
        1024 bytes = 2^10 -> 6
        """
        return int((math.log(blockSize) / math.log(2))) - 4

    def validSZX(cls, szx):
        return 0 <= szx <= 6

    def __str__(self):
        return "NUM: {%d}, SZX: {%d} ({%d} bytes), M: %b" % self.getNUM(),\
               self.SZX, self.size, self.M
