# coding=utf-8
"""
Testing endpoint features.
"""

import unittest
import pycolo as coap
from pycolo.endpoint import Endpoint, Rule


class BasicFunctionalityTestCase(unittest.TestCase):
    """
    Basic routing and endpoint testing
    """

    def setUp(self):
        """
        Set up a simple Endpoint. All the settings will be done
        in the further tests.
        """
        self.server = Endpoint(__name__)

    def test_request_dispatching(self):
        """
        Simple request dispatching
        """
        def index(request):
            """
            Simple mirror view
            :param request: Incoming request
            """
            return request.method

        self.server.route("/", index)
        self.server.route("/more", index, methods=['GET', 'POST'])

        self.assertEqual(coap.get(self.server.url + '/').data, 'GET')
        self.assertEqual(coap.post(self.server.url + '/').status_code, 405)
        self.assertEqual(coap.get(self.server.url + '/').status_code, 200)
        self.assertEqual(coap.post(self.server.url + '/more').data, 'POST')
        self.assertEqual(coap.get(self.server.url + '/more').data, 'GET')
        self.assertEqual(
            coap.delete(self.server.url + '/more').status_code,
            405)

    def test_url_mapping(self):
        """
        Simple URL mapping
        """
        method = lambda request: request.method

        self.server.add_url_rule('/', 'index', method)
        self.server.add_url_rule('/more', 'more', method,
            methods=['GET', 'POST'])
        self.assertEqual(coap.get(self.server.url + '/').data, 'GET')

        rv = coap.post(self.server.url + '/')
        self.assertEqual(rv.status_code, 405)

        rv = coap.delete(self.server.url + '/more')
        self.assertEqual(rv.status_code, 405)

    def test_routing(self):
        """
        Routing testing
        """
        self.server.url_map.add(('/foo', [
            Rule('/bar', endpoint='bar'),
            Rule('/', endpoint='index')
        ]))

        self.server.view_functions['bar'] = lambda: "bar"
        self.server.view_functions['index'] = lambda: "index"

        self.assertEqual(coap.get('/foo/').data, 'index')
        self.assertEqual(coap.get('/foo/bar').data, 'bar')

    def test_endpoint_decorator(self):
        """
        Test sub rule
        """
        self.server.url_map.add(
            ('/foo', [
                Rule('/bar', endpoint='bar'),
                Rule('/', endpoint='index')
            ]))

        self.server.destination('bar', lambda: "bar")
        self.server.destination('index', lambda: "index")

        self.assertEqual(coap.get('/foo/').data, "index")
        self.assertEqual(coap.get('/foo/bar').data, "bar")

    def test_error_handling(self):
        """
        Testing of the exception in the Endpoint
        """

        self.server.errorhandler(404, 'not found')
        self.server.errorhandler(500, 'internal server error')

        def index():
            """
            not_found called
            """
            self.server.abort(404)

        def error():
            """
            internal_server_error called
            """
            return 1 // 0

        self.server.route('/', index)
        self.server.route("/error", error)

        rv = coap.get(self.server.url + '/')
        self.assertEqual(rv.status_code, 404)
        self.assertEqual(rv.data, 'not found')

        rv = coap.get(self.server.url + '/error')
        self.assertEqual(rv.status_code, 500)
        self.assertEqual('internal server error', rv.data)

    def test_unicode(self):
        """
        Test unicode encoding
        """

        self.server.route('/unicode', lambda: 'Hällo Wörld')
        self.assertEqual(
            coap.get('/unicode').data,
            'Hällo Wörld'.encode())

    def test_max_content_length(self):
        """
        Test of the limitation of posting data on an endpoint

        :return:
        """
        self.server.config['MAX_CONTENT_LENGTH'] = 64
        rv = coap.post('/accept', data={'my_file': 'foo' * 100})
        self.assertEqual(rv.data, '42')

if __name__ == '__main__':
    unittest.main()
