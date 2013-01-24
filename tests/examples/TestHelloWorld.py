# coding=utf-8

"""
Simple Hello World example
"""

import unittest
from pycolo import codes
from pycolo.endpoint import Endpoint
from pycolo.api import request


class HelloWorldTest(unittest.TestCase):
    """
    Testsuite for unicode
    """
    message = "Hello World! My name is Rémy Léone look @ the funny € from UTF-8 (•‿•)"

    def setUp(self):
        """
        Setup a simple server with an hello world resource.

        Defines a resource that returns text with special characters on GET.
        """
        self.server = Endpoint(__name__)

        @self.server.route("/hello",
            title="Hello-World Resource",
            rt="HelloWorld")
        def hello():
            return self.message


    def test_simple_get(self):
        """
        Test a simple GET
        """
        r = request.get(self.server.url + "/.well-known/core")
        self.assertEqual(codes.ok, r.code)
        self.assertEqual(r.payload, self.message)


if __name__ == '__main__':
    unittest.main()
