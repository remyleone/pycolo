# coding=utf-8
import unittest

class TokenEqualityTest(unittest.TestCase):
    def testEmptyToken(self):
        pass

    #        t1 = option([None] * 0, options.TOKEN)
    #        t2 = option([None] * 0, options.TOKEN)
    #        self.assertEquals(t1, t2)
    #        self.assertEquals(0, t1.getLength())
    #        t3 = option("Not empty", options.TOKEN)
    #        self.assertNotEqual(t1, t3)

    def testOneByteToken(self):
        pass

    #        t1 = option(0xAB, options.TOKEN)
    #        t2 = option(0xAB, options.TOKEN)
    #        self.assertEquals(t1, t2)
    #        self.assertEquals(1, t1.getLength())
    #        t3 = option(0xAC, options.TOKEN)
    #        self.assertNotEqual(t1, t3)

    def testTwoByteToken(self):
        pass

    #        t1 = option(0xABCD, options.TOKEN)
    #        t2 = option(0xABCD, options.TOKEN)
    #        self.assertEquals(t1, t2)
    #        self.assertEquals(2, t1.getLength())
    #        t3 = option(0xABCE, options.TOKEN)
    #        self.assertNotEqual(t1, t3)

    def testFourByteToken(self):
        pass

    #        t1 = option(0xABCDEF01, options.TOKEN)
#        t2 = option(0xABCDEF01, options.TOKEN)
#        self.assertEquals(t1, t2)
#        self.assertEquals(4, t1.getLength())
#        t3 = option(0xABCDEF02, options.TOKEN)
#        self.assertNotEqual(t1, t3)

if __name__ == '__main__':
    unittest.main()