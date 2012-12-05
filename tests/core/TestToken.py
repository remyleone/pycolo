# coding=utf-8

"""
TODO
"""

import unittest

class TokenEqualityTest(unittest.TestCase):
    """
    TODO
    """

    def testEmptyToken(self):
        """
        TODO
        """
        pass

    #        t1 = option([None] * 0, options.TOKEN)
    #        t2 = option([None] * 0, options.TOKEN)
    #        self.assertEquals(t1, t2)
    #        self.assertEquals(0, t1.getLength())
    #        t3 = option("Not empty", options.TOKEN)
    #        self.assertNotEqual(t1, t3)

    def testOneByteToken(self):
        """
        TODO
        """
        pass

    #        t1 = option(0xAB, options.TOKEN)
    #        t2 = option(0xAB, options.TOKEN)
    #        self.assertEquals(t1, t2)
    #        self.assertEquals(1, t1.getLength())
    #        t3 = option(0xAC, options.TOKEN)
    #        self.assertNotEqual(t1, t3)

    def testTwoByteToken(self):
        """
        TODO
        """
        pass

    #        t1 = option(0xABCD, options.TOKEN)
    #        t2 = option(0xABCD, options.TOKEN)
    #        self.assertEquals(t1, t2)
    #        self.assertEquals(2, t1.getLength())
    #        t3 = option(0xABCE, options.TOKEN)
    #        self.assertNotEqual(t1, t3)

    def testFourByteToken(self):
        """
        TODO
        """
        pass

    #        t1 = option(0xABCDEF01, options.TOKEN)
#        t2 = option(0xABCDEF01, options.TOKEN)
#        self.assertEquals(t1, t2)
#        self.assertEquals(4, t1.getLength())
#        t3 = option(0xABCDEF02, options.TOKEN)
#        self.assertNotEqual(t1, t3)

    def test_token(self):
        """
        Check token.

        :param expectedToken the expected token
        :param actualToken the actual token
        :return True, if successful
        """
        #
        #success = True

        #        if expextedOption.equals(new Option(TokenManager.emptyToken, options.TOKEN)):
        #            self.assertEqual(None, actualOption)
        #        else:
        #            success = actualOption.getRawValue().length <= 8
        #            success &= actualOption.getRawValue().length >= 1
        #
        #        # eval token length
        #        if not success:
        #            logging.info("FAIL: Expected token %s, but %s has illegal length" % expextedOption, actualOption)
        #
        #        success &= expextedOption.toString().equals(actualOption.toString())


if __name__ == '__main__':
    unittest.main()