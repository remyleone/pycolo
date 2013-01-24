# coding=utf-8

"""
This test implement mix of HTTP request to a JSON API and CoAP server
serving this information.
"""

from urllib.request import urlopen
import unittest
from pycolo.endpoint import Endpoint
import pycolo as coap
from pycolo.observe import redis_observer

publish = redis_observer.publish
subscribe = redis_observer.subscribe


class TestWebCoAP(unittest.TestCase):
    """
    Interface CoAP, HTTP and observing in a simple weather setting.
    """

    def setUp(self):
        """
        Set up a loop to fetch the weather.
        :return:
        """
        self.server = Endpoint(__name__)

        def weather(self):
            """
            Infinite loop checking weather on a exterior website
            """
            while True:
                r = urlopen("http://openweather.com/")
                publish(content=r.readall())

        self.server.add_url_rule("/weather",
                              function=weather,
                              observable=True,
                              t=["json", "text"],
                              title="GET the current weather in Paris")

    def test_simple_get(self):
        """
        Simple get
        """
        temp = coap.get(self.server.url + "/weather")
        self.assertTrue(-50 < temp < 50)

    def test_simple_observe(self):
        """
        Simple observe
        """
        obs = coap.observe(self.server.url + "/weather",
                           sub=subscribe)
        for item in obs.listen(5):
            self.assertTrue(-50 < item < 50)


if __name__ == '__main__':
    unittest.main()
