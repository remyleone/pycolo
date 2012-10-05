# coding=utf-8
import unittest
from pycolo import Option

from pycolo.codes import options

class TokenEqualityTest(unittest.TestCase):

    def testEmptyToken(self):
        """ generated source for method testEmptyToken """
        t1 = Option([None] * 0, options.TOKEN)
        t2 = Option([None] * 0, options.TOKEN)
        self.assertEquals(t1, t2)
        self.assertEquals(0, t1.getLength())
        t3 = Option("Not empty", options.TOKEN)
        self.assertNotEqual(t1, t3)

    def testOneByteToken(self):
        """ generated source for method testOneByteToken """
        t1 = Option(0xAB, options.TOKEN)
        t2 = Option(0xAB, options.TOKEN)
        self.assertEquals(t1, t2)
        self.assertEquals(1, t1.getLength())
        t3 = Option(0xAC, options.TOKEN)
        self.assertNotEqual(t1, t3)

    def testTwoByteToken(self):
        """ generated source for method testTwoByteToken """
        t1 = Option(0xABCD, options.TOKEN)
        t2 = Option(0xABCD, options.TOKEN)
        self.assertEquals(t1, t2)
        self.assertEquals(2, t1.getLength())
        t3 = Option(0xABCE, options.TOKEN)
        self.assertNotEqual(t1, t3)

    def testFourByteToken(self):
        """ generated source for method testFourByteToken """
        t1 = Option(0xABCDEF01, options.TOKEN)
        t2 = Option(0xABCDEF01, options.TOKEN)
        self.assertEquals(t1, t2)
        self.assertEquals(4, t1.getLength())
        t3 = Option(0xABCDEF02, options.TOKEN)
        self.assertNotEqual(t1, t3)

if __name__ == '__main__':
    unittest.main()
