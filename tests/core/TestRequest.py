# coding=utf-8

"""
Testing CoAP requests
"""
import json
import os
import tempfile
import unittest

import pycolo as coap
from pycolo.request import request
from pycolo.endpoint import Endpoint
from pycolo.exceptions import InvalidURL, COAPError
from tests.examples.TestCoAPbin import coapbin


class CarelessTest(unittest.TestCase):
    """
    Careless testing suite
    """

    def setUp(self):
        """
        Set up of a careless server for request testing
        """
        self.server = Endpoint(__name__)

        def careless(self, request):
            """
            This implements a 'separate' resource for demonstration purposes.
            Defines a resource that returns a response in a separate CoAP
            Message

            1 °) promise the client that this request will be acted upon
            by sending an Acknowledgement...

            :param request:
            """
            request.accept()  # ... and then do nothing. Pretty mean.

        self.server.route("careless",
                      title="This resource will ACK anything, "
                            "but never send a separate response",
                      resourceType="SeparateResponseTester",
                      function=careless)

    def test_careless(self):
        """
        todo
        """
        pass


class RequestTestSuite(unittest.TestCase):
    """
    Request testing suite
    """

    def setUp(self):
        """
        Set up of the test set
        """
        self.coapbin = coapbin(__name__)

    def test_invalid_url(self):
        """
        Test for invalid URL
        """
        self.assertRaises(ValueError, coap.get("foobar"))

    def test_path_is_not_double_encoded(self):
        """
        Double encoding testing
        """
        r = coap.get(self.coapbin("/get/test case"))
        self.assertEqual(r.path_url, "/get/test%20case")

    def test_params_are_added_before_fragment(self):
        """
        Testing the correct order or url encoding
        """
        r = request(
            "coap://example.com/path#fragment", params={"a": "b"})
        self.assertEqual(r.full_url,
            "coap://example.com/path?a=b#fragment")
        r = request(
            "coap://example.com/path?key=value#fragment", params={"a": "b"})
        self.assertEqual(r.full_url,
            "coap://example.com/path?key=value&a=b#fragment")

    def test_params_accepts_kv_list(self):
        """
        Testing parameters encoding
        """
        r = request('coap://example.com/path',
                params=[('a', 'b')])
        self.assertEqual(r.full_url, 'coap://example.com/path?a=b')

    def test_200_OK_GET(self):
        """
        Testing OK status
        """
        self.assertEqual(coap.get(self.coapbin('get')).status_code,
                         200)

    def test_response_sent(self):
        """
        Testing "sent" status
        """
        r = coap.get(self.coapbin('get'))
        self.assertTrue(r.sent)

    def test_302_ALLOW_REDIRECT_GET(self):
        """
        Testing redirection
        """
        self.assertEqual(coap.get(self.coapbin('redirect', '1')).status_code,
                         200)

    def test_COAP_302_GET(self):
        """
        Testing redirection
        """
        r = coap.get(self.coapbin('redirect', '1'), allow_redirects=False)
        self.assertEqual(r.status_code, 302)

    def test_COAP_200_OK_GET_WITH_MIXED_PARAMS(self):
        """
        Test encoding coming from different sources
        """
        r = coap.get(self.coapbin('get') + '?test=true',
                     params={'q': 'test'},
                     headers={'User-agent': 'pycolo'})
        self.assertEqual(r.status_code, 200)

    def test_COAP_200_OK_PUT(self):
        """
        Test PUT request
        """
        r = coap.put(self.coapbin('put'))
        self.assertEqual(r.status_code, 200)

    def test_POST_FILES(self):
        """
        Test POST of text, files...
        """
        url = self.coapbin('post')

        post1 = coap.post(url, data={'some': 'data'})
        self.assertEqual(post1.status_code, 200)

        with open(__file__) as f:
            post2 = coap.post(url, files={'some': f})
            post3 = coap.post(url, files=[('some', f)])
        self.assertEqual(post2.status_code, 200)
        self.assertEqual(post3.status_code, 200)

        post4 = coap.post(url, data=json.dumps({"some": "json"}))
        self.assertEqual(post4.status_code, 200)

        try:
            coap.post(url, files=['bad file data'])
        except ValueError:
            pass

    def test_POST_FILES_WITH_PARAMS(self):
        """
        Test POST of files with parameters
        """
        with open(__file__) as f:
            url = self.coapbin('post')
            post1 = coap.post(url,
                              data={'some': 'data'},
                              files={'some': f})
            post2 = coap.post(url,
                              data={'some': 'data'},
                              files=[('some', f)])
            post3 = coap.post(url,
                              data=[('some', 'data')],
                              files=[('some', f)])

        self.assertEqual(post1.status_code, 200)
        self.assertEqual(post2.status_code, 200)
        self.assertEqual(post3.status_code, 200)

    def test_POST_FILES_WITH_CJK_PARAMS(self):
        """
        Test good unicode support for parameters in a POST request.
        """
        with open(__file__) as f:
            url = self.coapbin('post')
            post1 = coap.post(url, data={'some': '中文'}, files={'some': f})
            post2 = coap.post(url, data={'some': '日本語'}, files=[('some', f)])
            post3 = coap.post(url, data=[('some', '한국의')], files=[('some', f)])

        self.assertEqual(post1.status_code, 200)
        self.assertEqual(post2.status_code, 200)
        self.assertEqual(post3.status_code, 200)

    def test_POST_FILES_WITH_HEADERS(self):
        """
        Test POST with headers
        """
        url = self.coapbin('post')

        with open(__file__) as f:

            post2 = coap.post(url,
                files={'some': f})

        self.assertEqual(post2.status_code, 200)

    def test_nonzero_evaluation(self):
        """
        Test boolean support
        """
        r = coap.get(self.coapbin('status', '500'))
        self.assertEqual(bool(r), False)

        r = coap.get(self.coapbin('/get'))
        self.assertEqual(bool(r), True)

    def test_request_ok_set(self):
        """
        Test ok support
        """
        r = coap.get(self.coapbin('status', '404'))
        self.assertEqual(r.ok, False)

    def test_status_raising(self):
        """
        Test for basic exception support
        """
        r = coap.get(self.coapbin('status', '404'))
        self.assertRaises(COAPError, r.raise_for_status)

        r = coap.get(self.coapbin('status', '200'))
        self.assertFalse(r.error)
        r.raise_for_status()

    def test_default_status_raising(self):
        """
        Test for default exception
        """
        config = {'danger_mode': True}
        args = [self.coapbin('status', '404')]
        kwargs = {"config": config}
        self.assertRaises(COAPError, coap.get, *args, **kwargs)

        r = coap.get(self.coapbin('status', '200'))
        self.assertEqual(r.status_code, 200)

    def test_response_has_unicode_url(self):
        """
        Testing unicode URL
        """
        url = self.coapbin('get')
        response = coap.get(url)
        coap.get(url, params={'foo': 'føø'})
        coap.get(url, params={'føø': 'føø'})
        coap.get(url, params={'føø': 'føø'})
        coap.get(url, params={'foo': 'foo'})
        coap.get(self.coapbin('ø'), params={'foo': 'foo'})
        self.assertTrue(isinstance(response.url, str))

    def test_url_encoded_post_data(self):
        """
        Test post data
        """
        content = "foobar"
        r = coap.post(self.coapbin('post'), data={"test": content})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertEqual(r.url, self.coapbin('post'))

        raw_body = json.loads(r.text)

        self.assertEqual(raw_body.get('data'), '')

    def test_file_post_data(self):
        """
        Posting data
        """
        file_content = b"foobar"
        testfile = tempfile.NamedTemporaryFile(delete=False)
        testfile.write(file_content)
        testfile.flush()
        testfile.close()

        data = open(testfile.name, "rb")
        r = coap.post(self.coapbin('post'), data=data,
                headers={"content-type": "application/octet-stream"})

        data.close()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertEqual(r.url, self.coapbin('post'))

        raw_body = json.loads(r.text)
        self.assertTrue(raw_body.get('form') in (None, {}))
        self.assertEqual(raw_body.get('data'), file_content.decode('ascii'))
        os.remove(testfile.name)

    def test_url_encoded_post_querystring(self):
        """
        Testing query in URL
        """
        content = "foobar"
        r = coap.post(self.coapbin('post'), params={"test": content})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertEqual(r.url, self.coapbin('post?test=' + content))

        raw_body = json.loads(r.text)
        self.assertEqual(raw_body.get('form'), {})  # No form supplied
        self.assertEqual(raw_body.get('data'), '')

    def test_url_encoded_post_query(self):
        """
        Testing query and data in url
        """
        r = coap.post(
            self.coapbin('post'),
                params={"test": 'foo'})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertEqual(r.url, self.coapbin('post?test=foo'))

        r = coap.get(self.coapbin('get'), params={"test": ['foo', 'baz']})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.url, self.coapbin('get?test=foo&test=baz'))

    def test_url_encoded_post_querystring_multivalued(self):
        """
        todo
        """
        r = coap.post(self.coapbin('post'), params={"test": ['foo', 'baz']})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertEqual(r.url, self.coapbin('post?test=foo&test=baz'))

        raw_body = json.loads(r.text)
        self.assertEqual(raw_body.get('form'), {})  # No form supplied
        self.assertEqual(raw_body.get('data'), '')

    def test_url_encoded_post_query_multivalued_and_data(self):
        """
        todo
        """
        r = coap.post(
            self.coapbin('post'),
            params={"test": ['foo', 'baz']},
            data={"test2": "foobar",
                  "test3": ['foo', 'baz']})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertEqual(r.url, self.coapbin('post?test=foo&test=baz'))

        raw_body = json.loads(r.text)
        self.assertEqual(raw_body.get('form'),
                         {"test2": 'foobar',
                          "test3": ['foo', 'baz']})
        self.assertEqual(raw_body.get('data'), '')

    def test_multivalued_data_encoding(self):
        """
        Make sure data encoding works on a value that is an iterable but not
        a list
        """
        r = coap.post(
            self.coapbin('post'),
            data={"test": ('foo', "non_ascii")})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')

        raw_body = json.loads(r.text)
        self.assertEqual(raw_body.get('form'),
                         {"test": ['foo', "non_ascii"]})

    def test_GET_no_redirect(self):
        """
        todo
        """
        r = coap.get(self.coapbin('redirect', '3'), allow_redirects=False)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(len(r.history), 0)

    def test_redirect_history(self):
        """
        todo
        """
        r = coap.get(self.coapbin('redirect', '3'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.history), 3)

    def test_relative_redirect_history(self):
        """
        todo
        """
        r = coap.get(self.coapbin('relative-redirect', '3'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.history), 3)

    def test_session_COAP_200_OK_GET(self):
        """
        todo
        """
        s = coap.session()
        r = coap.get(self.coapbin('get'), session=s)
        self.assertEqual(r.status_code, 200)

    def test_session_persistent_params(self):
        """
        todo
        """
        params = {'a': 'a_test'}

        s = coap.session()
        s.params = params

        # Make 2 requests from Session object, should send header both times
        r1 = coap.get(self.coapbin('get'), session=s)
        self.assertTrue(params['a'] in r1.text)

        params2 = {'b': 'b_test'}

        r2 = coap.get(self.coapbin('get'), params=params2, session=s)
        for param in (params['a'], params2['b']):
            self.assertTrue(param in r2.text)

        params3 = {'b': 'b_test', 'a': None, 'c': 'c_test'}

        r3 = coap.get(self.coapbin('get'), params=params3, session=s)

        self.assertFalse(params['a'] in r3.text)

        for param in (params3['b'], params3['c']):
            self.assertTrue(param in r3.text)

    def test_session_connection_error_with_safe_mode(self):
        """
        todo
        """
        config = {"safe_mode": True}

        s = coap.session()
        r = s.get("coap://localhost:1/nope", timeout=0.1, config=config)
        self.assertFalse(r.ok)
        self.assertTrue(r.content is None)

        s2 = coap.session(config=config)
        r2 = s2.get("coap://localhost:1/nope", timeout=0.1)
        self.assertFalse(r2.ok)
        self.assertTrue(r2.content is None)

    def test_connection_error(self):
        """
        todo
        """
        try:
            coap.get('coap://localhost:1/nope')
        except coap.ConnectionError:
            pass
        else:
            self.fail()

    def test_cached_response(self):
        """
        todo
        """
        r1 = coap.get(self.coapbin('get'), prefetch=False)
        self.assertFalse(r1._content)
        self.assertTrue(r1.content)
        self.assertTrue(r1.text)

        r2 = coap.get(self.coapbin('get'), prefetch=True)
        self.assertTrue(r2._content)
        self.assertTrue(r2.content)
        self.assertTrue(r2.text)

    def test_iterate_lines(self):
        """
        todo
        """
        lines = (0, 2, 10, 100)

        for i in lines:
            r = coap.get(self.coapbin('stream', str(i)), prefetch=False)
            lines = list(r.iter_lines())
            len_lines = len(lines)

            self.assertEqual(i, len_lines)

        # Tests that trailing whitespaces within lines do not get stripped.
        # Tests that a trailing non-terminated line does not get stripped.
        quote = (
            '''foobar \n'''
            '''\t foobar \r\n'''
            '''\t '''
        )

        # Make a request and monkey-patch its contents
        r = coap.get(self.coapbin('get'), prefetch=False)

        lines = list(r.iter_lines())
        len_lines = len(lines)
        self.assertEqual(len_lines, 3)

        joined = lines[0] + '\n' + lines[1] + '\r\n' + lines[2]
        self.assertEqual(joined, quote)

    def test_permissive_iterate_content(self):
        """
        Test that iterate_content and iterate_lines work even after the body
        has been fetched.
        """
        r = coap.get(self.coapbin('stream', '10'), prefetch=True)
        self.assertTrue(r._content_consumed)
        # iterate_lines should still work without crashing
        self.assertEqual(len(list(r.iter_lines())), 10)

        # iterate_content should return a one-item iterator over the whole
        # content
        iterate_content_list = list(r.iter_content(chunk_size=1))
        self.assertTrue(all(len(item) == 1 for item in iterate_content_list))
        # when joined, it should be exactly the original content
        self.assertEqual(bytes().join(iterate_content_list), r.content)

        # test different chunk sizes:
        for chunk_size in range(2, 20):
            self.assertEqual(
                bytes().join(r.iter_content(chunk_size=chunk_size)),
                r.content)

    def test_safe_mode(self):
        """
        todo
        """
        safe = coap.session(config={"safe_mode": True})

        # Safe mode creates empty responses for failed requests.
        # Iterating on these responses should produce empty sequences
        r = coap.get('coap://0.0.0.0:700/', session=safe)
        self.assertEqual(list(r.iter_lines()), [])
        assert isinstance(r.error, coap.exceptions.ConnectionError)

        r = coap.get('coap://0.0.0.0:789/', session=safe)
        self.assertEqual(list(r.iter_content()), [])
        assert isinstance(r.error, coap.exceptions.ConnectionError)

        # When not in safe mode, should raise Timeout exception
        self.assertRaises(
             coap.exceptions.Timeout,
             coap.get,
             self.coapbin('stream', '1000'), timeout=0.0001)

        # In safe mode, should return a blank response
        r = coap.get(self.coapbin('stream', '1000'), timeout=0.0001,
                 config={"safe_mode": True})
        assert r.content is None
        assert isinstance(r.error, coap.exceptions.Timeout)

    def test_upload_binary_data(self):
        """
        todo
        """
        coap.get(self.coapbin('post'), data='\xff')

    def test_useful_exception_for_invalid_port(self):
        """
        If we pass a legitimate URL with an invalid port, we should fail.
        """
        self.assertRaises(
              ValueError,
              coap.get, 'coap://google.com:banana')

    def test_useful_exception_for_invalid_scheme(self):
        """
        If we pass a legitimate URL with a scheme not supported by requests,
        we should fail.
        """
        self.assertRaises(
              ValueError,
              coap.get,
              'ftp://ftp.kernel.org/pub/')

    def test_empty_response(self):
        """
        Test empty response in case of an error
        """
        r = coap.get(self.coapbin('status', '404'))
        self.assertIsNotNone(r.text)

    def test_post_fields_with_multiple_values_and_files(self):
        """
        Test that it is possible to POST using the files argument and a
        list for a value in the data argument.
        """
        data = {'field': ['a', 'b']}
        files = {'field': 'Garbled data'}
        r = coap.post(self.coapbin('post'), data=data, files=files)
        t = json.loads(r.text)
        self.assertEqual(t.get('form'), {'field': ['a', 'b']})
        self.assertEqual(t.get('files'), files)
        coap.post(self.coapbin('post'), data=data, files=files.items())
        self.assertEqual(t.get('files'), files)

    def test_str_data_content_type(self):
        """
        todo
        """
        data = 'test string data'
        r = coap.post(self.coapbin('post'), data=data)
        t = json.loads(r.text)
        self.assertEqual(t.get('headers').get('Content-Type'), '')

    def test_prefetch_redirect_bug(self):
        """
        Test that prefetch persists across re directions.
        """
        res = coap.get(self.coapbin('redirect/2'), prefetch=False)
        # prefetch should persist across the redirect;
        # the content should not have been consumed
        self.assertFalse(res._content_consumed)
        first_line = next(res.iter_lines())
        self.assertTrue(first_line.strip().decode('utf-8').startswith('{'))

    def test_prefetch_return_response_interaction(self):
        """
        Test that prefetch can be overridden as a kwarg to `send`.
        """
        req = coap.get(self.coapbin('get'), return_response=False)
        req.send(prefetch=False)
        # content should not have been pre-fetched
        self.assertFalse(req.response._content_consumed)
        first_line = next(req.response.iter_lines())
        self.assertTrue(first_line.strip().decode('utf-8').startswith('{'))

    def test_accept_objects_with_string_representations_as_urls(self):
        """
        Test that URLs can be set to objects with string representations,
        e.g. for use with furl.
        """
        r = coap.get('/get')
        self.assertEqual(r.status_code, 200)

    def test_bytes_files(self):
        """
        Test that `bytes` can be used as the values of `files`.
        """
        coap.post(self.coapbin('post'), files={'test': b'test'})

    def test_invalid_urls_throw_requests_exception(self):
        """
        Test that URLs with invalid labels throw
        Requests.exceptions.InvalidURL instead of UnicodeError.
        """
        self.assertRaises(InvalidURL, coap.get('coap://.coap.me/'))

    def test_none_values_in_data_are_deleted(self):
        """
        Test that keys with None as the value are removed instead of
        being posted.
        """
        r = coap.post(
            self.coapbin('post'),
            data={'key1': 'value1', 'key2': None})
        values = r.json['form']
        self.assertEqual(values['key1'], 'value1')
        # The 'key2' key should not have been sent.
        self.assertTrue(values.get('key2') is None)


class TestSimpleRequest(unittest.TestCase):
    """
    Simple request from the draft
    """

    def setUp(self):
        """
        Set up a basic endpoint for CoAP message exchange
        """
        self.server = Endpoint(__name__)

    def test_piggyback(self):
        """

       Client  Server
          |      |
          |      |
          +----->|     Header: GET (T=CON, Code=1, MID=0x7d34)
          | GET  |   Uri-Path: "temperature"
          |      |
          |      |
          |<-----+     Header: 2.05 Content (T=ACK, Code=69, MID=0x7d34)
          | 2.05 |    Payload: "22.3 C"
          |      |


        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       | 1 | 0 |   1   |     GET=1     |          MID=0x7d34           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |  11   |  11   |      "temperature" (11 B) ...
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       | 1 | 2 |   0   |    2.05=69    |          MID=0x7d34           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |      "22.3 C" (6 B) ...
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

               Figure 16: Confirmable request; piggy-backed response

        :return:
        """
        sent_raw = b""
        received_raw = b""

        r = coap.get(self.server.url + "temperature",
            confirmable=True,
            messageID=0x7d34)
        self.assertEqual(r.sent.raw, sent_raw)
        self.assertEqual(r.raw, received_raw)

    def test_raw2(self):
        """
           Client  Server
              |      |
              |      |
              +----->|     Header: GET (T=CON, Code=1, MID=0x7d35)
              | GET  |      Token: 0x20
              |      |   Uri-Path: "temperature"
              |      |
              |      |
              |<-----+     Header: 2.05 Content (T=ACK, Code=69, MID=0x7d35)
              | 2.05 |      Token: 0x20
              |      |    Payload: "22.3 C"
              |      |


            0                   1                   2                   3
            0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           | 1 | 0 |   2   |     GET=1     |          MID=0x7d35           |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |   11   |  11   |      "temperature" (11 B) ...
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |   8    |   1   |     0x20      |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


            0                   1                   2                   3
            0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           | 1 | 2 |   1   |    2.05=69    |          MID=0x7d35           |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |Jump 15 = 0xf1 |  4    |   1   |     0x20      | "22.3 C" (6 B) ...
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

        :return:
        """
        sent_raw = b""
        received_raw = b""

        r = coap.get(self.server.url + "temperature",
            confirmable=True,
            messageID=0x7d34)
        self.assertEqual(r.sent.raw, sent_raw)
        self.assertEqual(r.raw, received_raw)


if __name__ == '__main__':
    unittest.main()
