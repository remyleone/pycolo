# coding=utf-8

"""
This test implement mix of HTTP request to a JSON API and CoAP server
serving this information.
"""

from urllib.request import urlopen
import unittest
from pycolo import Endpoint
from pycolo.request import request as coap

class TestWebCoAP(unittest.TestSuite):

    def setUp():
        server = Endpoint(__name__)

        @server.route("/meteo",
                    observable=True, t=["json", "text"], repeat=5,
                    title="GET the current weather in Paris")
        def meteo(self):
            r = urlopen("http://openweather.com/")
            return r.readall()

    def testSimpleObserve(self):
        meteo = coap.get(self.server.url + "/meteo")
        temp = meteo
        self.assertTrue(-50 < temp < 50)


if __name__ == '__main__':
    unittest.main()
