# coding=utf-8

"""
TODO
"""

import unittest
from pycolo.endpoint import Endpoint
from pycolo.request import request as coap


class CarelessResource(Resource):
    """
    This class implements a 'separate' resource for demonstration purposes.
    Defines a resource that returns a response in a separate CoAP Message
    """
    def __init__(self,
                 title="This resource will ACK anything, but never send a separate response",
                 resourceType="SeparateResponseTester"):
        """
        :type title: title of the resource
        """
        self.title = title
        self.resourceType = resourceType

    def performGET(self, request):
        """
        promise the client that this request will be acted upon
        by sending an Acknowledgement...
        :param request:
        """
        request.accept()
        #  ... and then do nothing. Pretty mean.


class RequestTest(unittest.TestCase):
    """
    TODO
    """
    class RespondTask():
        """
        TODO
        """
        pass
    #        def __init__(self, request, response):
    #            super(self.RespondTask, self).__init__()
    #            self.request = request
    #            self.response = response
    #
    #        def run(self):
    #            """ generated source for method run """
    #            self.request.respond(self.response)
    #            self.request.sendResponse()
    #
    #        request = request()
    #        response = Response()
    #
    #    handledResponse = Response()

    def testRespond(self):
        """
        TODO
        """
        pass

    #        #  Client Side ////////////////////////////////////////////////////////
    #        #  create new request with own response handler
    #        request = GETRequest()
    #        #  (...) send the request to server
    #        #  Server Side ////////////////////////////////////////////////////////
    #        #  (...) receive request from client
    #        #  create new response
    #        response = Response()
    #        #  respond to the request
    #        request.respond(response)
    #        request.sendResponse()
    #        #  Validation /////////////////////////////////////////////////////////
    #        #  check if response was handled correctly
    #        self.assertSame(response, self.handledResponse)

    def testReceiveResponse(self):
        """
        TODO
        """
        pass

    #        #  Client Side ////////////////////////////////////////////////////////
    #        request = GETRequest()
    #        #  enable response queue in order to perform receiveResponse() calls
    #        request.enableResponseQueue(True)
    #        #  (...) send the request to server
    #        #  Server Side ////////////////////////////////////////////////////////
    #        #  (...) receive request from client
    #        #  create new response
    #        response = Response()
    #        #  schedule delayed response (e.g. take some time for computation etc.)
    #        self.timer.schedule(self.RespondTask(request, response), 500)
    #        #  Client Side ////////////////////////////////////////////////////////
    #        #  block until response received
    #        receivedResponse = request.receiveResponse()
    #        #  Validation /////////////////////////////////////////////////////////
    #        #  check if response was received correctly
    #        self.assertSame(response, receivedResponse)

    def testTokenManager(self):
        """
        TODO
        """
        pass

    #        acquiredTokens = {}
#        emptyToken = [None] * 0
#        acquiredTokens.add(emptyToken)
#        print("Contains: %s" % acquiredTokens.contains(emptyToken))
#        acquiredTokens.remove(emptyToken)
#        print("Contains: %s" % acquiredTokens.contains(emptyToken))

class RequestTestSuite(unittest.TestCase):

    def test_invalid_url(self):
        self.assertRaises(ValueError, get, "hiwpefhipowhefopw")

    def test_path_is_not_double_encoded(self):
        request = requests.Request("http://0.0.0.0/get/test case")

        self.assertEqual(request.path_url, "/get/test%20case")

    def test_params_are_added_before_fragment(self):
        request = requests.Request(
            "http://example.com/path#fragment", params={"a": "b"})
        self.assertEqual(request.full_url,
            "http://example.com/path?a=b#fragment")
        request = requests.Request(
            "http://example.com/path?key=value#fragment", params={"a": "b"})
        self.assertEqual(request.full_url,
            "http://example.com/path?key=value&a=b#fragment")

    def test_params_accepts_kv_list(self):
        request = requests.Request('http://example.com/path',
                params=[('a', 'b')])
        self.assertEqual(request.full_url, 'http://example.com/path?a=b')

    def test_HTTP_200_OK_GET(self):
        r = get(httpbin('get'))
        self.assertEqual(r.status_code, 200)

    def test_response_sent(self):
        r = get(httpbin('get'))

        self.assertTrue(r.request.sent)

    def test_HTTP_302_ALLOW_REDIRECT_GET(self):
        r = get(httpbin('redirect', '1'))
        self.assertEqual(r.status_code, 200)

    def test_HTTP_302_GET(self):
        r = get(httpbin('redirect', '1'), allow_redirects=False)
        self.assertEqual(r.status_code, 302)

    def test_HTTP_200_OK_GET_WITH_PARAMS(self):
        heads = {'User-agent': 'Mozilla/5.0'}

        r = get(httpbin('user-agent'), headers=heads)

        self.assertTrue(heads['User-agent'] in r.text)
        self.assertEqual(r.status_code, 200)

    def test_HTTP_200_OK_GET_WITH_MIXED_PARAMS(self):
        heads = {'User-agent': 'Mozilla/5.0'}

        r = get(httpbin('get') + '?test=true', params={'q': 'test'}, headers=heads)
        self.assertEqual(r.status_code, 200)

    def test_HTTP_200_OK_HEAD(self):
        r = head(httpbin('get'))
        self.assertEqual(r.status_code, 200)

    def test_HTTP_200_OK_PUT(self):
        r = put(httpbin('put'))
        self.assertEqual(r.status_code, 200)

    def test_POSTBIN_GET_POST_FILES(self):

        for service in SERVICES:

            url = service('post')
            post1 = post(url).raise_for_status()

            post1 = post(url, data={'some': 'data'})
            self.assertEqual(post1.status_code, 200)

            with open(__file__) as f:
                post2 = post(url, files={'some': f})
                post3 = post(url, files=[('some', f)])
            self.assertEqual(post2.status_code, 200)
            self.assertEqual(post3.status_code, 200)

            post4 = post(url, data='[{"some": "json"}]')
            self.assertEqual(post4.status_code, 200)

            try:
                post(url, files=['bad file data'])
            except ValueError:
                pass

    def test_POSTBIN_GET_POST_FILES_WITH_PARAMS(self):

        for service in SERVICES:

            with open(__file__) as f:
                url = service('post')
                post1 = post(url, data={'some': 'data'}, files={'some': f})
                post2 = post(url, data={'some': 'data'}, files=[('some', f)])
                post3 = post(url, data=[('some', 'data')], files=[('some', f)])

            self.assertEqual(post1.status_code, 200)
            self.assertEqual(post2.status_code, 200)
            self.assertEqual(post3.status_code, 200)

    def test_POSTBIN_GET_POST_FILES_WITH_CJK_PARAMS(self):

        for service in SERVICES:

            with open(__file__) as f:
                url = service('post')
                post1 = post(url, data={'some': '中文'}, files={'some': f})
                post2 = post(url, data={'some': '日本語'}, files=[('some', f)])
                post3 = post(url, data=[('some', '한국의')], files=[('some', f)])

            self.assertEqual(post1.status_code, 200)
            self.assertEqual(post2.status_code, 200)
            self.assertEqual(post3.status_code, 200)

    def test_POSTBIN_GET_POST_FILES_WITH_HEADERS(self):

        for service in SERVICES:

            url = service('post')

            with open(__file__) as f:

                post2 = post(url,
                    files={'some': f},
                    headers={'User-Agent': 'requests-tests'})

            self.assertEqual(post2.status_code, 200)

    def test_POSTBIN_GET_POST_FILES_STRINGS(self):

        for service in SERVICES:

            url = service('post')

            post1 = post(url, files={'fname.txt': 'fdata'})
            self.assertEqual(post1.status_code, 200)

            post2 = post(url, files={'fname.txt': 'fdata',
                    'fname2.txt': 'more fdata'})
            self.assertEqual(post2.status_code, 200)

            post3 = post(url, files={'fname.txt': 'fdata',
                    'fname2.txt': open(__file__, 'rb')})
            self.assertEqual(post3.status_code, 200)

            post4 = post(url, files={'fname.txt': 'fdata'})
            self.assertEqual(post4.status_code, 200)

            post5 = post(url, files={'file': ('file.txt', 'more fdata')})
            self.assertEqual(post5.status_code, 200)

            # Dirty hack to tide us over until 3.3.
            # TODO: Remove this hack when Python 3.3 is released.
            if (sys.version_info[0] == 2):
                fdata = '\xc3\xa9'.decode('utf-8')
            else:
                fdata = '\xe9'

            post6 = post(url, files={'fname.txt': fdata})
            self.assertEqual(post6.status_code, 200)

            post7 = post(url, files={'fname.txt': 'fdata to verify'})
            rbody = json.loads(post7.text)
            self.assertTrue(rbody.get('files', None))
            self.assertTrue(rbody['files'].get('fname.txt', None))
            self.assertEqual(rbody['files']['fname.txt'], 'fdata to verify')

            post8 = post(url, files=[('fname.txt', 'fdata')])
            self.assertEqual(post8.status_code, 200)
            resp_body = post8.json
            self.assertTrue(resp_body.get('files', None))
            self.assertTrue(resp_body['files'].get('fname.txt', None))
            self.assertEqual(resp_body['files']['fname.txt'], 'fdata')

            post9 = post(url, files=[('fname.txt', fdata)])
            self.assertEqual(post9.status_code, 200)

            post10 = post(url, files=[('file',
                        ('file.txt', 'more file data'))])
            self.assertEqual(post10.status_code, 200)

            post11 = post(url, files=[('fname.txt', 'fdata'),
                    ('fname2.txt', 'more fdata')])
            post12 = post(url, files=[('fname.txt', 'fdata'),
                    ('fname2.txt', open(__file__, 'rb'))])
            self.assertEqual(post11.status_code, 200)
            self.assertEqual(post12.status_code, 200)

    def test_nonzero_evaluation(self):

        for service in SERVICES:

            r = get(service('status', '500'))
            self.assertEqual(bool(r), False)

            r = get(service('/get'))
            self.assertEqual(bool(r), True)

    def test_request_ok_set(self):

        for service in SERVICES:

            r = get(service('status', '404'))
            # print r.status_code
            # r.raise_for_status()
            self.assertEqual(r.ok, False)

    def test_status_raising(self):
        r = get(httpbin('status', '404'))
        self.assertRaises(HTTPError, r.raise_for_status)

        r = get(httpbin('status', '200'))
        self.assertFalse(r.error)
        r.raise_for_status()

    def test_default_status_raising(self):
        config = {'danger_mode': True}
        args = [httpbin('status', '404')]
        kwargs = dict(config=config)
        self.assertRaises(HTTPError, get, *args, **kwargs)

        r = get(httpbin('status', '200'))
        self.assertEqual(r.status_code, 200)

    def test_decompress_gzip(self):

        r = get(httpbin('gzip'))
        r.content.decode('ascii')

    def test_response_has_unicode_url(self):

        for service in SERVICES:

            url = service('get')

            response = get(url)

            self.assertTrue(isinstance(response.url, str))

    def test_unicode_get(self):

        for service in SERVICES:

            url = service('/get')

            get(url, params={'foo': 'føø'})
            get(url, params={'føø': 'føø'})
            get(url, params={'føø': 'føø'})
            get(url, params={'foo': 'foo'})
            get(service('ø'), params={'foo': 'foo'})


    def test_urlencoded_post_data(self):

        for service in SERVICES:

            r = post(service('post'), data=dict(test='fooaowpeuf'))

            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers['content-type'], 'application/json')
            self.assertEqual(r.url, service('post'))

            rbody = json.loads(r.text)

            self.assertEqual(rbody.get('form'), dict(test='fooaowpeuf'))
            self.assertEqual(rbody.get('data'), '')

    def test_nonurlencoded_post_data(self):

        for service in SERVICES:

            r = post(service('post'), data='fooaowpeuf')

            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers['content-type'], 'application/json')
            self.assertEqual(r.url, service('post'))

            rbody = json.loads(r.text)
            # Body wasn't valid url encoded data, so the server returns None as
            # "form" and the raw body as "data".

            self.assertTrue(rbody.get('form') in (None, {}))
            self.assertEqual(rbody.get('data'), 'fooaowpeuf')

    def test_file_post_data(self):

        filecontent = b"fooaowpeufbarasjhf"
        testfile = tempfile.NamedTemporaryFile(delete=False)
        testfile.write(filecontent)
        testfile.flush()
        testfile.close()

        for service in SERVICES:

            data = open(testfile.name, "rb")
            r = post(service('post'), data=data,
                    headers={"content-type": "application/octet-stream"})

            data.close()
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers['content-type'], 'application/json')
            self.assertEqual(r.url, service('post'))

            rbody = json.loads(r.text)
            self.assertTrue(rbody.get('form') in (None, {}))
            self.assertEqual(rbody.get('data'), filecontent.decode('ascii'))
        os.remove(testfile.name)

    def test_urlencoded_post_querystring(self):

        for service in SERVICES:

            r = post(service('post'), params=dict(test='fooaowpeuf'))

            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers['content-type'], 'application/json')
            self.assertEqual(r.url, service('post?test=fooaowpeuf'))

            rbody = json.loads(r.text)
            self.assertEqual(rbody.get('form'), {})  # No form supplied
            self.assertEqual(rbody.get('data'), '')

    def test_urlencoded_post_query_and_data(self):

        for service in SERVICES:

            r = post(
                service('post'),
                params=dict(test='fooaowpeuf'),
                data=dict(test2="foobar"))

            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers['content-type'], 'application/json')
            self.assertEqual(r.url, service('post?test=fooaowpeuf'))

            rbody = json.loads(r.text)
            self.assertEqual(rbody.get('form'), dict(test2='foobar'))
            self.assertEqual(rbody.get('data'), '')

    def test_nonurlencoded_postdata(self):

        for service in SERVICES:

            r = post(service('post'), data="foobar")

            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers['content-type'], 'application/json')

            rbody = json.loads(r.text)

            self.assertTrue(rbody.get('form') in (None, {}))
            self.assertEqual(rbody.get('data'), 'foobar')

    def test_urlencoded_get_query_multivalued_param(self):

        for service in SERVICES:

            r = get(service('get'), params=dict(test=['foo', 'baz']))
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.url, service('get?test=foo&test=baz'))

    def test_urlencoded_post_querystring_multivalued(self):

        for service in SERVICES:

            r = post(service('post'), params=dict(test=['foo', 'baz']))
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers['content-type'], 'application/json')
            self.assertEqual(r.url, service('post?test=foo&test=baz'))

            rbody = json.loads(r.text)
            self.assertEqual(rbody.get('form'), {})  # No form supplied
            self.assertEqual(rbody.get('data'), '')

    def test_urlencoded_post_query_multivalued_and_data(self):

        for service in SERVICES:

            r = post(
                service('post'),
                params=dict(test=['foo', 'baz']),
                data=dict(test2="foobar", test3=['foo', 'baz']))

            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers['content-type'], 'application/json')
            self.assertEqual(r.url, service('post?test=foo&test=baz'))

            # print(r.text)
            # print('-----------------------')

            rbody = json.loads(r.text)
            self.assertEqual(rbody.get('form'), dict(test2='foobar', test3=['foo', 'baz']))
            self.assertEqual(rbody.get('data'), '')

    def test_multivalued_data_encoding(self):
        """
        Make sure data encoding works on a value that is an iterable but not
        a list
        """
        for service in SERVICES:
            # Can't have unicode literals in Python3, so avoid them.
            # TODO: fixup when moving to Python 3.3
            if (sys.version_info[0] == 2):
                nonascii = '\xc3\xa9'.decode('utf-8')
            else:
                nonascii = '\xe9'

            r = post(
                service('post'),
                data=dict(test=('foo', nonascii)))

            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers['content-type'], 'application/json')

            rbody = json.loads(r.text)
            self.assertEqual(rbody.get('form'),
                             dict(test=['foo', nonascii]))

    def test_GET_no_redirect(self):

        for service in SERVICES:

            r = get(service('redirect', '3'), allow_redirects=False)
            self.assertEqual(r.status_code, 302)
            self.assertEqual(len(r.history), 0)

    def test_HEAD_no_redirect(self):

        for service in SERVICES:

            r = head(service('redirect', '3'), allow_redirects=False)
            self.assertEqual(r.status_code, 302)
            self.assertEqual(len(r.history), 0)

    def test_redirect_history(self):

        for service in SERVICES:

            r = get(service('redirect', '3'))
            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.history), 3)

    def test_relative_redirect_history(self):

        for service in SERVICES:

            r = get(service('relative-redirect', '3'))
            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.history), 3)

    def test_session_HTTP_200_OK_GET(self):

        s = requests.session()
        r = get(httpbin('get'), session=s)
        self.assertEqual(r.status_code, 200)

    def test_session_persistent_headers(self):

        heads = {'User-agent': 'Mozilla/5.0'}

        s = requests.session()
        s.headers = heads

        # Make 2 requests from Session object, should send header both times
        r1 = get(httpbin('user-agent'), session=s)
        self.assertTrue(heads['User-agent'] in r1.text)

        r2 = get(httpbin('user-agent'), session=s)
        self.assertTrue(heads['User-agent'] in r2.text)

        new_heads = {'User-agent': 'blah'}
        r3 = get(httpbin('user-agent'), headers=new_heads, session=s)
        self.assertTrue(new_heads['User-agent'] in r3.text)

        self.assertEqual(r2.status_code, 200)

    def test_single_hook(self):

        def add_foo_header(args):
            if not args.get('headers'):
                args['headers'] = {}

            args['headers'].update({
                'X-Foo': 'foo'
            })

            return args

        for service in SERVICES:
            url = service('headers')
            response = get(url=url, hooks={'args': add_foo_header})

            self.assertTrue('foo' in response.text)

    def test_multiple_hooks(self):

        def add_foo_header(args):
            if not args.get('headers'):
                args['headers'] = {}

            args['headers'].update({
                'X-Foo': 'foo'
            })

            return args

        def add_bar_header(args):
            if not args.get('headers'):
                args['headers'] = {}

            args['headers'].update({
                'X-Bar': 'bar'
            })

            return args

        for service in SERVICES:
            url = service('headers')

            response = get(url=url,
                hooks={
                    'args': [add_foo_header, add_bar_header]
                }
            )

            for text in ('foo', 'bar'):
                self.assertTrue(text in response.text)

    def test_allow_list_of_hooks_to_register_hook(self):
        """Issue 785: https://github.com/kennethreitz/requests/issues/785"""
        def add_foo_header(args):
            if not args.get('headers'):
                args['headers'] = {}

            args['headers'].update({
                'X-Foo': 'foo'
            })

            return args

        def add_bar_header(args):
            if not args.get('headers'):
                args['headers'] = {}

            args['headers'].update({
                'X-Bar': 'bar'
            })

            return args

        def assert_hooks_are_callable(hooks):
            for h in hooks['args']:
                self.assertTrue(isinstance(h, collections.Callable))

        hooks = [add_foo_header, add_bar_header]
        r = requests.models.Request()
        r.register_hook('args', hooks)
        assert_hooks_are_callable(r.hooks)

        r = requests.models.Request(hooks={'args': hooks})
        assert_hooks_are_callable(r.hooks)

        hooks.append('string that should not be registered')
        r = requests.models.Request(hooks={'args': hooks})
        assert_hooks_are_callable(r.hooks)

    def test_session_persistent_cookies(self):

        s = requests.session()

        # Internally dispatched cookies are sent.
        _c = {'kenneth': 'reitz', 'bessie': 'monke'}
        r = get(httpbin('cookies'), cookies=_c, session=s)
        r = get(httpbin('cookies'), session=s)

        # Those cookies persist transparently.
        c = json.loads(r.text).get('cookies')
        self.assertEqual(c, _c)

        # Double check.
        r = get(httpbin('cookies'), cookies={}, session=s)
        c = json.loads(r.text).get('cookies')
        self.assertEqual(c, _c)

        # Remove a cookie by setting it's value to None.
        r = get(httpbin('cookies'), cookies={'bessie': None}, session=s)
        c = json.loads(r.text).get('cookies')
        del _c['bessie']
        self.assertEqual(c, _c)

        # Test session-level cookies.
        s = requests.session(cookies=_c)
        r = get(httpbin('cookies'), session=s)
        c = json.loads(r.text).get('cookies')
        self.assertEqual(c, _c)

        # Have the server set a cookie.
        r = get(httpbin('cookies', 'set', 'k', 'v'), allow_redirects=True, session=s)
        c = json.loads(r.text).get('cookies')

        self.assertTrue('k' in c)

        # And server-set cookie persistience.
        r = get(httpbin('cookies'), session=s)
        c = json.loads(r.text).get('cookies')

        self.assertTrue('k' in c)

    def test_session_persistent_params(self):

        params = {'a': 'a_test'}

        s = requests.session()
        s.params = params

        # Make 2 requests from Session object, should send header both times
        r1 = get(httpbin('get'), session=s)
        self.assertTrue(params['a'] in r1.text)

        params2 = {'b': 'b_test'}

        r2 = get(httpbin('get'), params=params2, session=s)
        for param in (params['a'], params2['b']):
            self.assertTrue(param in r2.text)

        params3 = {'b': 'b_test', 'a': None, 'c': 'c_test'}

        r3 = get(httpbin('get'), params=params3, session=s)

        self.assertFalse(params['a'] in r3.text)

        for param in (params3['b'], params3['c']):
            self.assertTrue(param in r3.text)

    def test_session_cookies_with_return_response_false(self):
        s = requests.session()
        # return_response=False as it does requests.async.get
        rq = get(httpbin('cookies', 'set', 'k', 'v'), return_response=False,
                 allow_redirects=True, session=s)
        rq.send(prefetch=True)
        c = rq.response.json.get('cookies')
        self.assertTrue('k' in c)
        self.assertTrue('k' in s.cookies)

    def test_session_pickling(self):

        s = requests.session(
                headers={'header': 'value'},
                cookies={'a-cookie': 'cookie-value'},
                auth=('username', 'password'))

        ds = pickle.loads(pickle.dumps(s))

        self.assertEqual(s.headers, ds.headers)
        self.assertEqual(s.auth, ds.auth)

        # Cookie doesn't have a good __eq__, so verify manually:
        self.assertEqual(len(ds.cookies), 1)
        for cookie in ds.cookies:
            self.assertCookieHas(cookie, name='a-cookie', value='cookie-value')

    def test_unpickled_session_requests(self):
        s = requests.session()
        r = get(httpbin('cookies', 'set', 'k', 'v'), allow_redirects=True, session=s)
        c = json.loads(r.text).get('cookies')
        self.assertTrue('k' in c)

        ds = pickle.loads(pickle.dumps(s))
        r = get(httpbin('cookies'), session=ds)
        c = json.loads(r.text).get('cookies')
        self.assertTrue('k' in c)

        ds1 = pickle.loads(pickle.dumps(requests.session()))
        ds2 = pickle.loads(pickle.dumps(requests.session(prefetch=False)))
        self.assertTrue(ds1.prefetch)
        self.assertFalse(ds2.prefetch)

    def test_session_connection_error_with_safe_mode(self):
        config = {"safe_mode":True}

        s = requests.session()
        r = s.get("http://localhost:1/nope", timeout=0.1, config=config)
        self.assertFalse(r.ok)
        self.assertTrue(r.content is None)

        s2 = requests.session(config=config)
        r2 = s2.get("http://localhost:1/nope", timeout=0.1)
        self.assertFalse(r2.ok)
        self.assertTrue(r2.content is None)

    def test_connection_error(self):
        try:
            get('http://localhost:1/nope')
        except requests.ConnectionError:
            pass
        else:
            self.fail()

    def test_connection_error_with_safe_mode(self):
        config = {'safe_mode': True}
        r = get('http://localhost:1/nope', allow_redirects=False, config=config)
        self.assertTrue(r.content is None)

    # def test_invalid_content(self):
    #     # WARNING: if you're using a terrible DNS provider (comcast),
    #     # this will fail.
    #     try:
    #         hah = 'http://somedomainthatclearlydoesntexistg.com'
    #         r = get(hah, allow_redirects=False)
    #     except requests.ConnectionError:
    #         pass   # \o/
    #     else:
    #         assert False

    #     config = {'safe_mode': True}
    #     r = get(hah, allow_redirects=False, config=config)
    #     assert r.content == None

    def test_cached_response(self):

        r1 = get(httpbin('get'), prefetch=False)
        self.assertFalse(r1._content)
        self.assertTrue(r1.content)
        self.assertTrue(r1.text)

        r2 = get(httpbin('get'), prefetch=True)
        self.assertTrue(r2._content)
        self.assertTrue(r2.content)
        self.assertTrue(r2.text)

    def test_iter_lines(self):

        lines = (0, 2, 10, 100)

        for i in lines:
            r = get(httpbin('stream', str(i)), prefetch=False)
            lines = list(r.iter_lines())
            len_lines = len(lines)

            self.assertEqual(i, len_lines)

        # Tests that trailing whitespaces within lines do not get stripped.
        # Tests that a trailing non-terminated line does not get stripped.
        quote = (
            '''Agamemnon  \n'''
            '''\tWhy will he not upon our fair request\r\n'''
            '''\tUntent his person and share the air with us?'''
        )

        # Make a request and monkey-patch its contents
        r = get(httpbin('get'), prefetch=False)
        r.raw = StringIO(quote)

        lines = list(r.iter_lines())
        len_lines = len(lines)
        self.assertEqual(len_lines, 3)

        joined = lines[0] + '\n' + lines[1] + '\r\n' + lines[2]
        self.assertEqual(joined, quote)

    def test_permissive_iter_content(self):
        """Test that iter_content and iter_lines work even after the body has been fetched."""
        r = get(httpbin('stream', '10'), prefetch=True)
        self.assertTrue(r._content_consumed)
        # iter_lines should still work without crashing
        self.assertEqual(len(list(r.iter_lines())), 10)

        # iter_content should return a one-item iterator over the whole content
        iter_content_list = list(r.iter_content(chunk_size=1))
        self.assertTrue(all(len(item) == 1 for item in iter_content_list))
        # when joined, it should be exactly the original content
        self.assertEqual(bytes().join(iter_content_list), r.content)

        # test different chunk sizes:
        for chunk_size in range(2, 20):
            self.assertEqual(bytes().join(r.iter_content(chunk_size=chunk_size)), r.content)


    # def test_safe_mode(self):

    #     safe = requests.session(config=dict(safe_mode=True))

    #     # Safe mode creates empty responses for failed requests.
    #     # Iterating on these responses should produce empty sequences
    #     r = get('http://0.0.0.0:700/', session=safe)
    #     self.assertEqual(list(r.iter_lines()), [])
    #     assert isinstance(r.error, requests.exceptions.ConnectionError)

    #     r = get('http://0.0.0.0:789/', session=safe)
    #     self.assertEqual(list(r.iter_content()), [])
    #     assert isinstance(r.error, requests.exceptions.ConnectionError)

    #     # When not in safe mode, should raise Timeout exception
    #     self.assertRaises(
    #         requests.exceptions.Timeout,
    #         get,
    #         httpbin('stream', '1000'), timeout=0.0001)

    #     # In safe mode, should return a blank response
    #     r = get(httpbin('stream', '1000'), timeout=0.0001,
    #             config=dict(safe_mode=True))
    #     assert r.content is None
    #     assert isinstance(r.error, requests.exceptions.Timeout)

    def test_upload_binary_data(self):

        requests.get(httpbin('post'), auth=('a', 'b'), data='\xff')

    def test_useful_exception_for_invalid_port(self):
        # If we pass a legitimate URL with an invalid port, we should fail.
        self.assertRaises(
              ValueError,
              get,
              'http://google.com:banana')

    def test_useful_exception_for_invalid_scheme(self):

        # If we pass a legitimate URL with a scheme not supported
        # by requests, we should fail.
        self.assertRaises(
              ValueError,
              get,
              'ftp://ftp.kernel.org/pub/')

    def test_can_have_none_in_header_values(self):
        try:
            # Don't choke on headers with none in the value.
            requests.get(httpbin('headers'), headers={'Foo': None})
        except TypeError:
            self.fail('Not able to have none in header values')

    def test_danger_mode_redirects(self):
        s = requests.session()
        s.config['danger_mode'] = True
        s.get(httpbin('redirect', '4'))

    def test_empty_response(self):
        r = requests.get(httpbin('status', '404'))
        r.text

    def test_max_redirects(self):
        """Test the max_redirects config variable, normally and under safe_mode."""
        def unsafe_callable():
            requests.get(httpbin('redirect', '3'), config=dict(max_redirects=2))
        self.assertRaises(requests.exceptions.TooManyRedirects, unsafe_callable)

        # add safe mode
        response = requests.get(httpbin('redirect', '3'), config=dict(safe_mode=True, max_redirects=2))
        self.assertTrue(response.content is None)
        self.assertTrue(isinstance(response.error, requests.exceptions.TooManyRedirects))

    def test_connection_keepalive_and_close(self):
        """Test that we send 'Connection: close' when keep_alive is disabled."""
        # keep-alive should be on by default
        r1 = requests.get(httpbin('get'))
        # XXX due to proxying issues, test the header sent back by httpbin, rather than
        # the header reported in its message body. See kennethreitz/httpbin#46
        self.assertEqual(r1.headers['Connection'].lower(), 'keep-alive')

        # but when we disable it, we should send a 'Connection: close'
        # and get the same back:
        r2 = requests.get(httpbin('get'), config=dict(keep_alive=False))
        self.assertEqual(r2.headers['Connection'].lower(), 'close')

    def test_head_content(self):
        """Test that empty bodies are properly supported."""

        r = requests.head(httpbin('headers'))
        r.content
        r.text

    def test_post_fields_with_multiple_values_and_files(self):
        """Test that it is possible to POST using the files argument and a
        list for a value in the data argument."""

        data = {'field': ['a', 'b']}
        files = {'field': 'Garbled data'}
        r = post(httpbin('post'), data=data, files=files)
        t = json.loads(r.text)
        self.assertEqual(t.get('form'), {'field': ['a', 'b']})
        self.assertEqual(t.get('files'), files)
        r = post(httpbin('post'), data=data, files=files.items())
        self.assertEqual(t.get('files'), files)

    def test_str_data_content_type(self):
        data = 'test string data'
        r = post(httpbin('post'), data=data)
        t = json.loads(r.text)
        self.assertEqual(t.get('headers').get('Content-Type'), '')

    def test_prefetch_redirect_bug(self):
        """Test that prefetch persists across redirections."""
        res = get(httpbin('redirect/2'), prefetch=False)
        # prefetch should persist across the redirect;
        # the content should not have been consumed
        self.assertFalse(res._content_consumed)
        first_line = next(res.iter_lines())
        self.assertTrue(first_line.strip().decode('utf-8').startswith('{'))

    def test_prefetch_return_response_interaction(self):
        """Test that prefetch can be overridden as a kwarg to `send`."""
        req = requests.get(httpbin('get'), return_response=False)
        req.send(prefetch=False)
        # content should not have been prefetched
        self.assertFalse(req.response._content_consumed)
        first_line = next(req.response.iter_lines())
        self.assertTrue(first_line.strip().decode('utf-8').startswith('{'))

    def test_accept_objects_with_string_representations_as_urls(self):
        """Test that URLs can be set to objects with string representations,
        e.g. for use with furl."""
        class URL():
            def __unicode__(self):
                # Can't have unicode literals in Python3, so avoid them.
                # TODO: fixup when moving to Python 3.3
                if (sys.version_info[0] == 2):
                    return 'http://httpbin.org/get'.decode('utf-8')
                else:
                    return 'http://httpbin.org/get'

            def __str__(self):
                return 'http://httpbin.org/get'

        r = get(URL())
        self.assertEqual(r.status_code, 200)

    def test_post_fields_with_multiple_values_and_files_as_tuples(self):
        """Test that it is possible to POST multiple data and file fields
        with the same name.
        https://github.com/kennethreitz/requests/pull/746
        """

        fields = [
            ('__field__', '__value__'),
            ('__field__', '__value__'),
        ]

        r = post(httpbin('post'), data=fields, files=fields)
        t = json.loads(r.text)

        self.assertEqual(t.get('form'), {
            '__field__': [
                '__value__',
                '__value__',
            ]
        })

        # It's not currently possible to test for multiple file fields with
        # the same name against httpbin so we need to inspect the encoded
        # body manually.
        request = r.request
        body, content_type = request._encode_files(request.files)
        file_field = (b'Content-Disposition: form-data;'
                      b' name="__field__"; filename="__field__"')
        self.assertEqual(body.count(b'__value__'), 4)
        self.assertEqual(body.count(file_field), 2)

    def test_bytes_files(self):
        """Test that `bytes` can be used as the values of `files`."""
        post(httpbin('post'), files={'test': b'test'})

    def test_invalid_urls_throw_requests_exception(self):
        """Test that URLs with invalid labels throw
        Requests.exceptions.InvalidURL instead of UnicodeError."""
        self.assertRaises(InvalidURL, get, 'http://.google.com/')

    def test_none_vals_in_data_are_deleted(self):
        """Test that keys with None as the value are removed instead of
        being posted."""
        data = {'key1': 'value1', 'key2': None}
        r = post(httpbin('post'), data=data)
        vals = r.json['form']
        self.assertEqual(vals['key1'], 'value1')
        # The 'key2' key should not have been sent.
        self.assertTrue(vals.get('key2') is None)


class TestSeparate(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        # sep = Separate()
        pass


class TestSimpleRequest(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        self.server = Endpoint()


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

        r = coap.get(self.server.url + "temperature", confirmable=True, messageID=0x7d34)
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

        r = coap.get(self.server.url + "temperature", confirmable=True, messageID=0x7d34)
        self.assertEqual(r.sent.raw, sent_raw)
        self.assertEqual(r.raw, received_raw)


if __name__ == '__main__':
    unittest.main()
