# coding=utf-8

def test_checkDiscovery(self, expextedAttribute, actualDiscovery):
    """
    Check discovery.

    :param expextedAttribute the resource attribute to filter
    :param actualDiscovery the reported Link Format
    :param actualDiscovery:
    :param expextedAttribute:
    :return True, if successful
    """

    # resource res = RemoteResource.newRoot(actualDiscovery)
    #
    # List < Option > query = new ArrayList < Option > ()
    # query.add(new Option(expextedAttribute, options.URI_QUERY))
    #
    # success = True
    #
    # for sub in res.getSubResources():
    #   success &= LinkFormat.matches(sub, query)
    #
    #       if not success:
    #           logging.info("FAIL: Expected %s, but was %s\n", expextedAttribute, LinkFormat.serialize(sub, null, false))
    #
    #            if success:
    #                logging.info("PASS: Correct Link Format filtering")

        # get requests
        response = client.get('/?foo=bar&foo=hehe')
        assert response['args'] == MultiDict([('foo', 'bar'), ('foo', 'hehe')])
        assert response['args_as_list'] == [('foo', ['bar', 'hehe'])]
        assert response['form'] == MultiDict()
        assert response['form_as_list'] == []
        assert response['data'] == ''
        self.assert_environ(response['environ'], 'GET')

        # post requests with form data
        response = client.post('/?blub=blah', data='foo=blub+hehe&blah=42',
                               content_type='application/x-www-form-urlencoded')
        assert response['args'] == MultiDict([('blub', 'blah')])
        assert response['args_as_list'] == [('blub', ['blah'])]
        assert response['form'] == MultiDict([('foo', 'blub hehe'), ('blah', '42')])
        assert response['data'] == ''
        
        # currently we do not guarantee that the values are ordered correctly
        # for post data.
        ## assert response['form_as_list'] == [('foo', ['blub hehe']), ('blah', ['42'])]
        self.assert_environ(response['environ'], 'POST')
        # post requests with json data
        json = '{"foo": "bar", "blub": "blah"}'
        response = client.post('/?a=b', data=json, content_type='application/json')
        assert response['data'] == json
        assert response['args'] == MultiDict([('a', 'b')])
        assert response['form'] == MultiDict()

    def test_url_request_descriptors(self):
        req = wrappers.Request.from_values('/bar?foo=baz', 'http://example.com/test')
        assert req.path == u'/bar'
        assert req.full_path == u'/bar?foo=baz'
        assert req.script_root == u'/test'
        assert req.url == 'http://example.com/test/bar?foo=baz'
        assert req.base_url == 'http://example.com/test/bar'
        assert req.url_root == 'http://example.com/test/'
        assert req.host_url == 'http://example.com/'
        assert req.host == 'example.com'
        assert req.scheme == 'http'
        req = wrappers.Request.from_values('/bar?foo=baz', 'https://example.com/test')
        assert req.scheme == 'https'
        
    def test_base_response(self):
        # unicode
        response = wrappers.BaseResponse(u'öäü')
        assert response.data == 'öäü'

        # writing
        response = wrappers.Response('foo')
        response.stream.write('bar')
        assert response.data == 'foobar'

        # set cookie
        response = wrappers.BaseResponse()
        response.set_cookie('foo', 'bar', 60, 0, '/blub', 'example.org', False)
        assert response.headers.to_list() == [
            ('Content-Type', 'text/plain; charset=utf-8'),
            ('Set-Cookie', 'foo=bar; Domain=example.org; expires=Thu, '
             '01-Jan-1970 00:00:00 GMT; Max-Age=60; Path=/blub')
        ]

        # delete cookie
        response = wrappers.BaseResponse()
        response.delete_cookie('foo')
        assert response.headers.to_list() == [
            ('Content-Type', 'text/plain; charset=utf-8'),
            ('Set-Cookie', 'foo=; expires=Thu, 01-Jan-1970 00:00:00 GMT; Max-Age=0; Path=/')
        ]

        # close call forwarding
        closed = []
        class Iterable(object):
            def next(self):
                raise StopIteration()
            def __iter__(self):
                return self
            def close(self):
                closed.append(True)
        response = wrappers.BaseResponse(Iterable())
        response.call_on_close(lambda: closed.append(True))
        app_iter, status, headers = run_wsgi_app(response,
                                                 create_environ(),
                                                 buffered=True)
        assert status == '200 OK'
        assert ''.join(app_iter) == ''
        assert len(closed) == 2

    def test_response_status_codes(self):
        response = wrappers.BaseResponse()
        response.status_code = 404
        assert response.status == '404 NOT FOUND'
        response.status = '200 OK'
        assert response.status_code == 200
        response.status = '999 WTF'
        assert response.status_code == 999
        response.status_code = 588
        assert response.status_code == 588
        assert response.status == '588 UNKNOWN'
        response.status = 'wtf'
        assert response.status_code == 0

    def test_etag_response_mixin(self):
        response = wrappers.Response('Hello World')
        assert response.get_etag() == (None, None)
        response.add_etag()
        assert response.get_etag() == ('b10a8db164e0754105b7a99be72e3fe5', False)
        assert not response.cache_control
        response.cache_control.must_revalidate = True
        response.cache_control.max_age = 60
        response.headers['Content-Length'] = len(response.data)
        assert response.headers['Cache-Control'] == 'must-revalidate, max-age=60'

        assert 'date' not in response.headers
        env = create_environ()
        env.update({
            'REQUEST_METHOD':       'GET',
            'HTTP_IF_NONE_MATCH':   response.get_etag()[0]
        })
        response.make_conditional(env)
        assert 'date' in response.headers

        # after the thing is invoked by the server as wsgi application
        # (we're emulating this here), there must not be any entity
        # headers left and the status code would have to be 304
        resp = wrappers.Response.from_app(response, env)
        assert resp.status_code == 304
        assert not 'content-length' in resp.headers

        # make sure date is not overriden
        response = wrappers.Response('Hello World')
        response.date = 1337
        d = response.date
        response.make_conditional(env)
        assert response.date == d

        # make sure content length is only set if missing
        response = wrappers.Response('Hello World')
        response.content_length = 999
        response.make_conditional(env)
        self.assert_equal(response.content_length, 999)

    def test_etag_response_mixin_freezing(self):
        class WithFreeze(wrappers.ETagResponseMixin, wrappers.BaseResponse):
            pass
        class WithoutFreeze(wrappers.BaseResponse, wrappers.ETagResponseMixin):
            pass

        response = WithFreeze('Hello World')
        response.freeze()
        assert response.get_etag() == (wrappers.generate_etag('Hello World'), False)
        response = WithoutFreeze('Hello World')
        response.freeze()
        assert response.get_etag() == (None, None)
        response = wrappers.Response('Hello World')
        response.freeze()
        assert response.get_etag() == (None, None)

    def test_urlfication(self):
        resp = wrappers.Response()
        resp.headers['Location'] = u'http://üser:pässword@☃.net/påth'
        resp.headers['Content-Location'] = u'http://☃.net/'
        headers = resp.get_wsgi_headers(create_environ())
        assert headers['location'] == \
            'http://%C3%BCser:p%C3%A4ssword@xn--n3h.net/p%C3%A5th'
        assert headers['content-location'] == 'http://xn--n3h.net/'

class URLsTestCase(WerkzeugTestCase):

    def test_quoting(self):
        assert urls.url_quote(u'\xf6\xe4\xfc') == '%C3%B6%C3%A4%C3%BC'
        assert urls.url_unquote(urls.url_quote(u'#%="\xf6')) == u'#%="\xf6'
        assert urls.url_quote_plus('foo bar') == 'foo+bar'
        assert urls.url_unquote_plus('foo+bar') == 'foo bar'
        assert urls.url_encode({'a': None, 'b': 'foo bar'}) == 'b=foo+bar'
        assert urls.url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)') == \
               'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    def test_url_decoding(self):
        x = urls.url_decode('foo=42&bar=23&uni=H%C3%A4nsel')
        assert x['foo'] == '42'
        assert x['bar'] == '23'
        assert x['uni'] == u'Hänsel'

        x = urls.url_decode('foo=42;bar=23;uni=H%C3%A4nsel', separator=';')
        assert x['foo'] == '42'
        assert x['bar'] == '23'
        assert x['uni'] == u'Hänsel'

        x = urls.url_decode('%C3%9Ch=H%C3%A4nsel', decode_keys=True)
        assert x[u'Üh'] == u'Hänsel'

    def test_streamed_url_decoding(self):
        item1 = 'a' * 100000
        item2 = 'b' * 400
        string = 'a=%s&b=%s&c=%s' % (item1, item2, item2)
        gen = urls.url_decode_stream(StringIO(string), limit=len(string),
                                     return_iterator=True)
        self.assert_equal(gen.next(), ('a', item1))
        self.assert_equal(gen.next(), ('b', item2))
        self.assert_equal(gen.next(), ('c', item2))
        self.assert_raises(StopIteration, gen.next)

    def test_url_encoding(self):
        assert urls.url_encode({'foo': 'bar 45'}) == 'foo=bar+45'
        d = {'foo': 1, 'bar': 23, 'blah': u'Hänsel'}
        assert urls.url_encode(d, sort=True) == 'bar=23&blah=H%C3%A4nsel&foo=1'
        assert urls.url_encode(d, sort=True, separator=';') == 'bar=23;blah=H%C3%A4nsel;foo=1'

    def test_sorted_url_encode(self):
        assert urls.url_encode({"a": 42, "b": 23, 1: 1, 2: 2}, sort=True) == '1=1&2=2&a=42&b=23'
        assert urls.url_encode({'A': 1, 'a': 2, 'B': 3, 'b': 4}, sort=True,
                          key=lambda x: x[0].lower()) == 'A=1&a=2&B=3&b=4'

    def test_streamed_url_encoding(self):
        out = StringIO()
        urls.url_encode_stream({'foo': 'bar 45'}, out)
        self.assert_equal(out.getvalue(), 'foo=bar+45')

        d = {'foo': 1, 'bar': 23, 'blah': u'Hänsel'}
        out = StringIO()
        urls.url_encode_stream(d, out, sort=True)
        self.assert_equal(out.getvalue(), 'bar=23&blah=H%C3%A4nsel&foo=1')
        out = StringIO()
        urls.url_encode_stream(d, out, sort=True, separator=';')
        self.assert_equal(out.getvalue(), 'bar=23;blah=H%C3%A4nsel;foo=1')

        gen = urls.url_encode_stream(d, sort=True)
        self.assert_equal(gen.next(), 'bar=23')
        self.assert_equal(gen.next(), 'blah=H%C3%A4nsel')
        self.assert_equal(gen.next(), 'foo=1')
        self.assert_raises(StopIteration, gen.next)

    def test_url_fixing(self):
        x = urls.url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffskl\xe4rung)')
        assert x == 'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

        x = urls.url_fix('http://example.com/?foo=%2f%2f')
        assert x == 'http://example.com/?foo=%2f%2f'

    def test_iri_support(self):
        self.assert_raises(UnicodeError, urls.uri_to_iri, u'http://föö.com/')
        self.assert_raises(UnicodeError, urls.iri_to_uri, 'http://föö.com/')
        assert urls.uri_to_iri('http://xn--n3h.net/') == u'http://\u2603.net/'
        assert urls.uri_to_iri('http://%C3%BCser:p%C3%A4ssword@xn--n3h.net/p%C3%A5th') == \
            u'http://\xfcser:p\xe4ssword@\u2603.net/p\xe5th'
        assert urls.iri_to_uri(u'http://☃.net/') == 'http://xn--n3h.net/'
        assert urls.iri_to_uri(u'http://üser:pässword@☃.net/påth') == \
            'http://%C3%BCser:p%C3%A4ssword@xn--n3h.net/p%C3%A5th'

        assert urls.uri_to_iri('http://test.com/%3Fmeh?foo=%26%2F') == \
            u'http://test.com/%3Fmeh?foo=%26%2F'

        # this should work as well, might break on 2.4 because of a broken
        # idna codec
        assert urls.uri_to_iri('/foo') == u'/foo'
        assert urls.iri_to_uri(u'/foo') == '/foo'

    def test_ordered_multidict_encoding(self):
        d = OrderedMultiDict()
        d.add('foo', 1)
        d.add('foo', 2)
        d.add('foo', 3)
        d.add('bar', 0)
        d.add('foo', 4)
        assert urls.url_encode(d) == 'foo=1&foo=2&foo=3&bar=0&foo=4'

    def test_href(self):
        x = urls.Href('http://www.example.com/')
        assert x('foo') == 'http://www.example.com/foo'
        assert x.foo('bar') == 'http://www.example.com/foo/bar'
        assert x.foo('bar', x=42) == 'http://www.example.com/foo/bar?x=42'
        assert x.foo('bar', class_=42) == 'http://www.example.com/foo/bar?class=42'
        assert x.foo('bar', {'class': 42}) == 'http://www.example.com/foo/bar?class=42'
        self.assert_raises(AttributeError, lambda: x.__blah__)

        x = urls.Href('blah')
        assert x.foo('bar') == 'blah/foo/bar'

        self.assert_raises(TypeError, x.foo, {"foo": 23}, x=42)

        x = urls.Href('')
        assert x('foo') == 'foo'

    def test_href_url_join(self):
        x = urls.Href('test')
        assert x('foo:bar') == 'test/foo:bar'
        assert x('http://example.com/') == 'test/http://example.com/'

    if 0:
        # stdlib bug? :(
        def test_href_past_root(self):
            base_href = urls.Href('http://www.blagga.com/1/2/3')
            assert base_href('../foo') == 'http://www.blagga.com/1/2/foo'
            assert base_href('../../foo') == 'http://www.blagga.com/1/foo'
            assert base_href('../../../foo') == 'http://www.blagga.com/foo'
            assert base_href('../../../../foo') == 'http://www.blagga.com/foo'
            assert base_href('../../../../../foo') == 'http://www.blagga.com/foo'
            assert base_href('../../../../../../foo') == 'http://www.blagga.com/foo'

    def test_url_unquote_plus_unicode(self):
        # was broken in 0.6
        assert urls.url_unquote_plus(u'\x6d') == u'\x6d'
        assert type(urls.url_unquote_plus(u'\x6d')) is unicode

    def test_quoting_of_local_urls(self):
        rv = urls.iri_to_uri(u'/foo\x8f')
        assert rv == '/foo%C2%8F'
        assert type(rv) is str

class RoutingTestCase(WerkzeugTestCase):

    def test_basic_routing(self):
        map = r.Map([
            r.Rule('/', endpoint='index'),
            r.Rule('/foo', endpoint='foo'),
            r.Rule('/bar/', endpoint='bar')
        ])
        adapter = map.bind('example.org', '/')
        assert adapter.match('/') == ('index', {})
        assert adapter.match('/foo') == ('foo', {})
        assert adapter.match('/bar/') == ('bar', {})
        self.assert_raises(r.RequestRedirect, lambda: adapter.match('/bar'))
        self.assert_raises(r.NotFound, lambda: adapter.match('/blub'))

        adapter = map.bind('example.org', '/test')
        try:
            adapter.match('/bar')
        except r.RequestRedirect, e:
            assert e.new_url == 'http://example.org/test/bar/'
        else:
            self.fail('Expected request redirect')

        adapter = map.bind('example.org', '/')
        try:
            adapter.match('/bar')
        except r.RequestRedirect, e:
            assert e.new_url == 'http://example.org/bar/'
        else:
            self.fail('Expected request redirect')

        adapter = map.bind('example.org', '/')
        try:
            adapter.match('/bar', query_args={'aha': 'muhaha'})
        except r.RequestRedirect, e:
            assert e.new_url == 'http://example.org/bar/?aha=muhaha'
        else:
            self.fail('Expected request redirect')

        adapter = map.bind('example.org', '/')
        try:
            adapter.match('/bar', query_args='aha=muhaha')
        except r.RequestRedirect, e:
            assert e.new_url == 'http://example.org/bar/?aha=muhaha'
        else:
            self.fail('Expected request redirect')

        adapter = map.bind_to_environ(create_environ('/bar?foo=bar',
                                                     'http://example.org/'))
        try:
            adapter.match()
        except r.RequestRedirect, e:
            assert e.new_url == 'http://example.org/bar/?foo=bar'
        else:
            self.fail('Expected request redirect')

    def test_environ_defaults(self):
        environ = create_environ("/foo")
        self.assert_equal(environ["PATH_INFO"], '/foo')
        m = r.Map([r.Rule("/foo", endpoint="foo"), r.Rule("/bar", endpoint="bar")])
        a = m.bind_to_environ(environ)
        self.assert_equal(a.match("/foo"), ('foo', {}))
        self.assert_equal(a.match(), ('foo', {}))
        self.assert_equal(a.match("/bar"), ('bar', {}))
        self.assert_raises(r.NotFound, a.match, "/bars")

    def test_basic_building(self):
        map = r.Map([
            r.Rule('/', endpoint='index'),
            r.Rule('/foo', endpoint='foo'),
            r.Rule('/bar/<baz>', endpoint='bar'),
            r.Rule('/bar/<int:bazi>', endpoint='bari'),
            r.Rule('/bar/<float:bazf>', endpoint='barf'),
            r.Rule('/bar/<path:bazp>', endpoint='barp'),
            r.Rule('/hehe', endpoint='blah', subdomain='blah')
        ])
        adapter = map.bind('example.org', '/', subdomain='blah')

        assert adapter.build('index', {}) == 'http://example.org/'
        assert adapter.build('foo', {}) == 'http://example.org/foo'
        assert adapter.build('bar', {'baz': 'blub'}) == 'http://example.org/bar/blub'
        assert adapter.build('bari', {'bazi': 50}) == 'http://example.org/bar/50'
        assert adapter.build('barf', {'bazf': 0.815}) == 'http://example.org/bar/0.815'
        assert adapter.build('barp', {'bazp': 'la/di'}) == 'http://example.org/bar/la/di'
        assert adapter.build('blah', {}) == '/hehe'
        self.assert_raises(r.BuildError, lambda: adapter.build('urks'))

        adapter = map.bind('example.org', '/test', subdomain='blah')
        assert adapter.build('index', {}) == 'http://example.org/test/'
        assert adapter.build('foo', {}) == 'http://example.org/test/foo'
        assert adapter.build('bar', {'baz': 'blub'}) == 'http://example.org/test/bar/blub'
        assert adapter.build('bari', {'bazi': 50}) == 'http://example.org/test/bar/50'
        assert adapter.build('barf', {'bazf': 0.815}) == 'http://example.org/test/bar/0.815'
        assert adapter.build('barp', {'bazp': 'la/di'}) == 'http://example.org/test/bar/la/di'
        assert adapter.build('blah', {}) == '/test/hehe'

    def test_defaults(self):
        map = r.Map([
            r.Rule('/foo/', defaults={'page': 1}, endpoint='foo'),
            r.Rule('/foo/<int:page>', endpoint='foo')
        ])
        adapter = map.bind('example.org', '/')

        assert adapter.match('/foo/') == ('foo', {'page': 1})
        self.assert_raises(r.RequestRedirect, lambda: adapter.match('/foo/1'))
        assert adapter.match('/foo/2') == ('foo', {'page': 2})
        assert adapter.build('foo', {}) == '/foo/'
        assert adapter.build('foo', {'page': 1}) == '/foo/'
        assert adapter.build('foo', {'page': 2}) == '/foo/2'

    def test_greedy(self):
        map = r.Map([
            r.Rule('/foo', endpoint='foo'),
            r.Rule('/<path:bar>', endpoint='bar'),
            r.Rule('/<path:bar>/<path:blub>', endpoint='bar')
        ])
        adapter = map.bind('example.org', '/')

        assert adapter.match('/foo') == ('foo', {})
        assert adapter.match('/blub') == ('bar', {'bar': 'blub'})
        assert adapter.match('/he/he') == ('bar', {'bar': 'he', 'blub': 'he'})

        assert adapter.build('foo', {}) == '/foo'
        assert adapter.build('bar', {'bar': 'blub'}) == '/blub'
        assert adapter.build('bar', {'bar': 'blub', 'blub': 'bar'}) == '/blub/bar'

    def test_path(self):
        map = r.Map([
            r.Rule('/', defaults={'name': 'FrontPage'}, endpoint='page'),
            r.Rule('/Special', endpoint='special'),
            r.Rule('/<int:year>', endpoint='year'),
            r.Rule('/<path:name>', endpoint='page'),
            r.Rule('/<path:name>/edit', endpoint='editpage'),
            r.Rule('/<path:name>/silly/<path:name2>', endpoint='sillypage'),
            r.Rule('/<path:name>/silly/<path:name2>/edit', endpoint='editsillypage'),
            r.Rule('/Talk:<path:name>', endpoint='talk'),
            r.Rule('/User:<username>', endpoint='user'),
            r.Rule('/User:<username>/<path:name>', endpoint='userpage'),
            r.Rule('/Files/<path:file>', endpoint='files'),
        ])
        adapter = map.bind('example.org', '/')

        assert adapter.match('/') == ('page', {'name':'FrontPage'})
        self.assert_raises(r.RequestRedirect, lambda: adapter.match('/FrontPage'))
        assert adapter.match('/Special') == ('special', {})
        assert adapter.match('/2007') == ('year', {'year':2007})
        assert adapter.match('/Some/Page') == ('page', {'name':'Some/Page'})
        assert adapter.match('/Some/Page/edit') == ('editpage', {'name':'Some/Page'})
        assert adapter.match('/Foo/silly/bar') == ('sillypage', {'name':'Foo', 'name2':'bar'})
        assert adapter.match('/Foo/silly/bar/edit') == ('editsillypage', {'name':'Foo', 'name2':'bar'})
        assert adapter.match('/Talk:Foo/Bar') == ('talk', {'name':'Foo/Bar'})
        assert adapter.match('/User:thomas') == ('user', {'username':'thomas'})
        assert adapter.match('/User:thomas/projects/werkzeug') == \
            ('userpage', {'username':'thomas', 'name':'projects/werkzeug'})
        assert adapter.match('/Files/downloads/werkzeug/0.2.zip') == \
            ('files', {'file':'downloads/werkzeug/0.2.zip'})

    def test_dispatch(self):
        env = create_environ('/')
        map = r.Map([
            r.Rule('/', endpoint='root'),
            r.Rule('/foo/', endpoint='foo')
        ])
        adapter = map.bind_to_environ(env)

        raise_this = None
        def view_func(endpoint, values):
            if raise_this is not None:
                raise raise_this
            return Response(repr((endpoint, values)))
        dispatch = lambda p, q=False: Response.force_type(adapter.dispatch(view_func, p,
                                                          catch_http_exceptions=q), env)

        assert dispatch('/').data == "('root', {})"
        assert dispatch('/foo').status_code == 301
        raise_this = r.NotFound()
        self.assert_raises(r.NotFound, lambda: dispatch('/bar'))
        assert dispatch('/bar', True).status_code == 404

    def test_http_host_before_server_name(self):
        env = {
            'HTTP_HOST':            'wiki.example.com',
            'SERVER_NAME':          'web0.example.com',
            'SERVER_PORT':          '80',
            'SCRIPT_NAME':          '',
            'PATH_INFO':            '',
            'REQUEST_METHOD':       'GET',
            'wsgi.url_scheme':      'http'
        }
        map = r.Map([r.Rule('/', endpoint='index', subdomain='wiki')])
        adapter = map.bind_to_environ(env, server_name='example.com')
        assert adapter.match('/') == ('index', {})
        assert adapter.build('index', force_external=True) == 'http://wiki.example.com/'
        assert adapter.build('index') == '/'

        env['HTTP_HOST'] = 'admin.example.com'
        adapter = map.bind_to_environ(env, server_name='example.com')
        assert adapter.build('index') == 'http://wiki.example.com/'

    def test_adapter_url_parameter_sorting(self):
        map = r.Map([r.Rule('/', endpoint='index')], sort_parameters=True,
                     sort_key=lambda x: x[1])
        adapter = map.bind('localhost', '/')
        assert adapter.build('index', {'x': 20, 'y': 10, 'z': 30},
            force_external=True) == 'http://localhost/?y=10&x=20&z=30'

    def test_request_direct_charset_bug(self):
        map = r.Map([r.Rule(u'/öäü/')])
        adapter = map.bind('localhost', '/')
        try:
            adapter.match(u'/öäü')
        except r.RequestRedirect, e:
            assert e.new_url == 'http://localhost/%C3%B6%C3%A4%C3%BC/'
        else:
            self.fail('expected request redirect exception')

    def test_request_redirect_default(self):
        map = r.Map([r.Rule(u'/foo', defaults={'bar': 42}),
                     r.Rule(u'/foo/<int:bar>')])
        adapter = map.bind('localhost', '/')
        try:
            adapter.match(u'/foo/42')
        except r.RequestRedirect, e:
            assert e.new_url == 'http://localhost/foo'
        else:
            self.fail('expected request redirect exception')

    def test_request_redirect_default_subdomain(self):
        map = r.Map([r.Rule(u'/foo', defaults={'bar': 42}, subdomain='test'),
                     r.Rule(u'/foo/<int:bar>', subdomain='other')])
        adapter = map.bind('localhost', '/', subdomain='other')
        try:
            adapter.match(u'/foo/42')
        except r.RequestRedirect, e:
            assert e.new_url == 'http://test.localhost/foo'
        else:
            self.fail('expected request redirect exception')

    def test_adapter_match_return_rule(self):
        rule = r.Rule('/foo/', endpoint='foo')
        map = r.Map([rule])
        adapter = map.bind('localhost', '/')
        assert adapter.match('/foo/', return_rule=True) == (rule, {})

    def test_server_name_interpolation(self):
        server_name = 'example.invalid'
        map = r.Map([r.Rule('/', endpoint='index'),
                     r.Rule('/', endpoint='alt', subdomain='alt')])

        env = create_environ('/', 'http://%s/' % server_name)
        adapter = map.bind_to_environ(env, server_name=server_name)
        assert adapter.match() == ('index', {})

        env = create_environ('/', 'http://alt.%s/' % server_name)
        adapter = map.bind_to_environ(env, server_name=server_name)
        assert adapter.match() == ('alt', {})

        env = create_environ('/', 'http://%s/' % server_name)
        adapter = map.bind_to_environ(env, server_name='foo')
        assert adapter.subdomain == '<invalid>'

    def test_rule_emptying(self):
        rule = r.Rule('/foo', {'meh': 'muh'}, 'x', ['POST'],
                   False, 'x', True, None)
        rule2 = rule.empty()
        assert rule.__dict__ == rule2.__dict__
        rule.methods.add('GET')
        assert rule.__dict__ != rule2.__dict__
        rule.methods.discard('GET')
        rule.defaults['meh'] = 'aha'
        assert rule.__dict__ != rule2.__dict__

    def test_rule_templates(self):
        testcase = r.RuleTemplate(
            [ r.Submount('/test/$app',
              [ r.Rule('/foo/', endpoint='handle_foo')
              , r.Rule('/bar/', endpoint='handle_bar')
              , r.Rule('/baz/', endpoint='handle_baz')
              ]),
              r.EndpointPrefix('${app}',
              [ r.Rule('/${app}-blah', endpoint='bar')
              , r.Rule('/${app}-meh', endpoint='baz')
              ]),
              r.Subdomain('$app',
              [ r.Rule('/blah', endpoint='x_bar')
              , r.Rule('/meh', endpoint='x_baz')
              ])
            ])

        url_map = r.Map(
            [ testcase(app='test1')
            , testcase(app='test2')
            , testcase(app='test3')
            , testcase(app='test4')
            ])

        out = sorted([(x.rule, x.subdomain, x.endpoint)
                      for x in url_map.iter_rules()])

        assert out == ([
            ('/blah', 'test1', 'x_bar'),
            ('/blah', 'test2', 'x_bar'),
            ('/blah', 'test3', 'x_bar'),
            ('/blah', 'test4', 'x_bar'),
            ('/meh', 'test1', 'x_baz'),
            ('/meh', 'test2', 'x_baz'),
            ('/meh', 'test3', 'x_baz'),
            ('/meh', 'test4', 'x_baz'),
            ('/test/test1/bar/', '', 'handle_bar'),
            ('/test/test1/baz/', '', 'handle_baz'),
            ('/test/test1/foo/', '', 'handle_foo'),
            ('/test/test2/bar/', '', 'handle_bar'),
            ('/test/test2/baz/', '', 'handle_baz'),
            ('/test/test2/foo/', '', 'handle_foo'),
            ('/test/test3/bar/', '', 'handle_bar'),
            ('/test/test3/baz/', '', 'handle_baz'),
            ('/test/test3/foo/', '', 'handle_foo'),
            ('/test/test4/bar/', '', 'handle_bar'),
            ('/test/test4/baz/', '', 'handle_baz'),
            ('/test/test4/foo/', '', 'handle_foo'),
            ('/test1-blah', '', 'test1bar'),
            ('/test1-meh', '', 'test1baz'),
            ('/test2-blah', '', 'test2bar'),
            ('/test2-meh', '', 'test2baz'),
            ('/test3-blah', '', 'test3bar'),
            ('/test3-meh', '', 'test3baz'),
            ('/test4-blah', '', 'test4bar'),
            ('/test4-meh', '', 'test4baz')
        ])

    def test_complex_routing_rules(self):
        m = r.Map([
            r.Rule('/', endpoint='index'),
            r.Rule('/<int:blub>', endpoint='an_int'),
            r.Rule('/<blub>', endpoint='a_string'),
            r.Rule('/foo/', endpoint='nested'),
            r.Rule('/foobar/', endpoint='nestedbar'),
            r.Rule('/foo/<path:testing>/', endpoint='nested_show'),
            r.Rule('/foo/<path:testing>/edit', endpoint='nested_edit'),
            r.Rule('/users/', endpoint='users', defaults={'page': 1}),
            r.Rule('/users/page/<int:page>', endpoint='users'),
            r.Rule('/foox', endpoint='foox'),
            r.Rule('/<path:bar>/<path:blub>', endpoint='barx_path_path')
        ])
        a = m.bind('example.com')

        assert a.match('/') == ('index', {})
        assert a.match('/42') == ('an_int', {'blub': 42})
        assert a.match('/blub') == ('a_string', {'blub': 'blub'})
        assert a.match('/foo/') == ('nested', {})
        assert a.match('/foobar/') == ('nestedbar', {})
        assert a.match('/foo/1/2/3/') == ('nested_show', {'testing': '1/2/3'})
        assert a.match('/foo/1/2/3/edit') == ('nested_edit', {'testing': '1/2/3'})
        assert a.match('/users/') == ('users', {'page': 1})
        assert a.match('/users/page/2') == ('users', {'page': 2})
        assert a.match('/foox') == ('foox', {})
        assert a.match('/1/2/3') == ('barx_path_path', {'bar': '1', 'blub': '2/3'})

        assert a.build('index') == '/'
        assert a.build('an_int', {'blub': 42}) == '/42'
        assert a.build('a_string', {'blub': 'test'}) == '/test'
        assert a.build('nested') == '/foo/'
        assert a.build('nestedbar') == '/foobar/'
        assert a.build('nested_show', {'testing': '1/2/3'}) == '/foo/1/2/3/'
        assert a.build('nested_edit', {'testing': '1/2/3'}) == '/foo/1/2/3/edit'
        assert a.build('users', {'page': 1}) == '/users/'
        assert a.build('users', {'page': 2}) == '/users/page/2'
        assert a.build('foox') == '/foox'
        assert a.build('barx_path_path', {'bar': '1', 'blub': '2/3'}) == '/1/2/3'

    def test_default_converters(self):
        class MyMap(r.Map):
            default_converters = r.Map.default_converters.copy()
            default_converters['foo'] = r.UnicodeConverter
        assert isinstance(r.Map.default_converters, ImmutableDict)
        m = MyMap([
            r.Rule('/a/<foo:a>', endpoint='a'),
            r.Rule('/b/<foo:b>', endpoint='b'),
            r.Rule('/c/<c>', endpoint='c')
        ], converters={'bar': r.UnicodeConverter})
        a = m.bind('example.org', '/')
        assert a.match('/a/1') == ('a', {'a': '1'})
        assert a.match('/b/2') == ('b', {'b': '2'})
        assert a.match('/c/3') == ('c', {'c': '3'})
        assert 'foo' not in r.Map.default_converters

    def test_build_append_unknown(self):
        map = r.Map([
            r.Rule('/bar/<float:bazf>', endpoint='barf')
        ])
        adapter = map.bind('example.org', '/', subdomain='blah')
        assert adapter.build('barf', {'bazf': 0.815, 'bif' : 1.0}) == \
            'http://example.org/bar/0.815?bif=1.0'
        assert adapter.build('barf', {'bazf': 0.815, 'bif' : 1.0},
            append_unknown=False) == 'http://example.org/bar/0.815'

    def test_method_fallback(self):
        map = r.Map([
            r.Rule('/', endpoint='index', methods=['GET']),
            r.Rule('/<name>', endpoint='hello_name', methods=['GET']),
            r.Rule('/select', endpoint='hello_select', methods=['POST']),
            r.Rule('/search_get', endpoint='search', methods=['GET']),
            r.Rule('/search_post', endpoint='search', methods=['POST'])
        ])
        adapter = map.bind('example.com')
        assert adapter.build('index') == '/'
        assert adapter.build('index', method='GET') == '/'
        assert adapter.build('hello_name', {'name': 'foo'}) == '/foo'
        assert adapter.build('hello_select') == '/select'
        assert adapter.build('hello_select', method='POST') == '/select'
        assert adapter.build('search') == '/search_get'
        assert adapter.build('search', method='GET') == '/search_get'
        assert adapter.build('search', method='POST') == '/search_post'

    def test_implicit_head(self):
        url_map = r.Map([
            r.Rule('/get', methods=['GET'], endpoint='a'),
            r.Rule('/post', methods=['POST'], endpoint='b')
        ])
        adapter = url_map.bind('example.org')
        assert adapter.match('/get', method='HEAD') == ('a', {})
        self.assert_raises(r.MethodNotAllowed, adapter.match,
                           '/post', method='HEAD')

    def test_protocol_joining_bug(self):
        m = r.Map([r.Rule('/<foo>', endpoint='x')])
        a = m.bind('example.org')
        assert a.build('x', {'foo': 'x:y'}) == '/x:y'
        assert a.build('x', {'foo': 'x:y'}, force_external=True) == \
            'http://example.org/x:y'

    def test_allowed_methods_querying(self):
        m = r.Map([r.Rule('/<foo>', methods=['GET', 'HEAD']),
                   r.Rule('/foo', methods=['POST'])])
        a = m.bind('example.org')
        assert sorted(a.allowed_methods('/foo')) == ['GET', 'HEAD', 'POST']

    def test_external_building_with_port(self):
        map = r.Map([
            r.Rule('/', endpoint='index'),
        ])
        adapter = map.bind('example.org:5000', '/')
        built_url = adapter.build('index', {}, force_external=True)
        assert built_url == 'http://example.org:5000/', built_url

    def test_external_building_with_port_bind_to_environ(self):
        map = r.Map([
            r.Rule('/', endpoint='index'),
        ])
        adapter = map.bind_to_environ(
            create_environ('/', 'http://example.org:5000/'),
            server_name="example.org:5000"
        )
        built_url = adapter.build('index', {}, force_external=True)
        assert built_url == 'http://example.org:5000/', built_url

    def test_external_building_with_port_bind_to_environ_wrong_servername(self):
        map = r.Map([
            r.Rule('/', endpoint='index'),
        ])
        environ = create_environ('/', 'http://example.org:5000/')
        adapter = map.bind_to_environ(environ, server_name="example.org")
        assert adapter.subdomain == '<invalid>'

    def test_converter_parser(self):
        args, kwargs = r.parse_converter_args(u'test, a=1, b=3.0')

        assert args == ('test',)
        assert kwargs == {'a': 1, 'b': 3.0 }

        args, kwargs = r.parse_converter_args('')
        assert not args and not kwargs

        args, kwargs = r.parse_converter_args('a, b, c,')
        assert args == ('a', 'b', 'c')
        assert not kwargs

        args, kwargs = r.parse_converter_args('True, False, None')
        assert args == (True, False, None)

        args, kwargs = r.parse_converter_args('"foo", u"bar"')
        assert args == ('foo', 'bar')

    def test_alias_redirects(self):
        m = r.Map([
            r.Rule('/', endpoint='index'),
            r.Rule('/index.html', endpoint='index', alias=True),
            r.Rule('/users/', defaults={'page': 1}, endpoint='users'),
            r.Rule('/users/index.html', defaults={'page': 1}, alias=True,
                   endpoint='users'),
            r.Rule('/users/page/<int:page>', endpoint='users'),
            r.Rule('/users/page-<int:page>.html', alias=True, endpoint='users'),
        ])
        a = m.bind('example.com')

        def ensure_redirect(path, new_url, args=None):
            try:
                a.match(path, query_args=args)
            except r.RequestRedirect, e:
                assert e.new_url == 'http://example.com' + new_url
            else:
                assert False, 'expected redirect'

        ensure_redirect('/index.html', '/')
        ensure_redirect('/users/index.html', '/users/')
        ensure_redirect('/users/page-2.html', '/users/page/2')
        ensure_redirect('/users/page-1.html', '/users/')
        ensure_redirect('/users/page-1.html', '/users/?foo=bar', {'foo': 'bar'})

        assert a.build('index') == '/'
        assert a.build('users', {'page': 1}) == '/users/'
        assert a.build('users', {'page': 2}) == '/users/page/2'

    def test_double_defaults(self):
        for prefix in '', '/aaa':
            m = r.Map([
                r.Rule(prefix + '/', defaults={'foo': 1, 'bar': False}, endpoint='x'),
                r.Rule(prefix + '/<int:foo>', defaults={'bar': False}, endpoint='x'),
                r.Rule(prefix + '/bar/', defaults={'foo': 1, 'bar': True}, endpoint='x'),
                r.Rule(prefix + '/bar/<int:foo>', defaults={'bar': True}, endpoint='x')
            ])
            a = m.bind('example.com')

            assert a.match(prefix + '/') == ('x', {'foo': 1, 'bar': False})
            assert a.match(prefix + '/2') == ('x', {'foo': 2, 'bar': False})
            assert a.match(prefix + '/bar/') == ('x', {'foo': 1, 'bar': True})
            assert a.match(prefix + '/bar/2') == ('x', {'foo': 2, 'bar': True})

            assert a.build('x', {'foo': 1, 'bar': False}) == prefix + '/'
            assert a.build('x', {'foo': 2, 'bar': False}) == prefix + '/2'
            assert a.build('x', {'bar': False}) == prefix + '/'
            assert a.build('x', {'foo': 1, 'bar': True}) == prefix + '/bar/'
            assert a.build('x', {'foo': 2, 'bar': True}) == prefix + '/bar/2'
            assert a.build('x', {'bar': True}) == prefix + '/bar/'

    def test_host_matching(self):
        m = r.Map([
            r.Rule('/', endpoint='index', host='www.<domain>'),
            r.Rule('/', endpoint='files', host='files.<domain>'),
            r.Rule('/foo/', defaults={'page': 1}, host='www.<domain>', endpoint='x'),
            r.Rule('/<int:page>', host='files.<domain>', endpoint='x')
        ], host_matching=True)

        a = m.bind('www.example.com')
        assert a.match('/') == ('index', {'domain': 'example.com'})
        assert a.match('/foo/') == ('x', {'domain': 'example.com', 'page': 1})
        try:
            a.match('/foo')
        except r.RequestRedirect, e:
            assert e.new_url == 'http://www.example.com/foo/'
        else:
            assert False, 'expected redirect'

        a = m.bind('files.example.com')
        assert a.match('/') == ('files', {'domain': 'example.com'})
        assert a.match('/2') == ('x', {'domain': 'example.com', 'page': 2})
        try:
            a.match('/1')
        except r.RequestRedirect, e:
            assert e.new_url == 'http://www.example.com/foo/'
        else:
            assert False, 'expected redirect'

    def test_server_name_casing(self):
        m = r.Map([
            r.Rule('/', endpoint='index', subdomain='foo')
        ])

        env = create_environ()
        env['SERVER_NAME'] = env['HTTP_HOST'] = 'FOO.EXAMPLE.COM'
        a = m.bind_to_environ(env, server_name='example.com')
        assert a.match('/') == ('index', {})

        env = create_environ()
        env['SERVER_NAME'] = '127.0.0.1'
        env['SERVER_PORT'] = '5000'
        del env['HTTP_HOST']
        a = m.bind_to_environ(env, server_name='example.com')
        try:
            a.match()
        except r.NotFound:
            pass
        else:
            assert False, 'Expected not found exception'

    def test_redirect_request_exception_code(self):
        exc = r.RequestRedirect('http://www.google.com/')
        exc.code = 307
        env = create_environ()
        self.assert_equal(exc.get_response(env).status_code, exc.code)

    def test_unicode_rules(self):
        m = r.Map([
            r.Rule(u'/войти/', endpoint='enter'),
            r.Rule(u'/foo+bar/', endpoint='foobar')
        ])
        a = m.bind(u'☃.example.com')
        try:
            a.match(u'/войти')
        except r.RequestRedirect, e:
            self.assert_equal(e.new_url, 'http://xn--n3h.example.com/'
                              '%D0%B2%D0%BE%D0%B9%D1%82%D0%B8/')
        endpoint, values = a.match(u'/войти/')
        self.assert_equal(endpoint, 'enter')
        self.assert_equal(values, {})

        try:
            a.match(u'/foo+bar')
        except r.RequestRedirect, e:
            self.assert_equal(e.new_url, 'http://xn--n3h.example.com/'
                              'foo+bar/')
        endpoint, values = a.match(u'/foo+bar/')
        self.assert_equal(endpoint, 'foobar')
        self.assert_equal(values, {})

        url = a.build('enter', {}, force_external=True)
        self.assert_equal(url, 'http://xn--n3h.example.com/%D0%B2%D0%BE%D0%B9%D1%82%D0%B8/')

        url = a.build('foobar', {}, force_external=True)
        self.assert_equal(url, 'http://xn--n3h.example.com/foo+bar/')

class BasicFunctionalityTestCase(FlaskTestCase):

    def test_options_work(self):
        app = flask.Flask(__name__)
        @app.route('/', methods=['GET', 'POST'])
        def index():
            return 'Hello World'
        rv = app.test_client().open('/', method='OPTIONS')
        self.assert_equal(sorted(rv.allow), ['GET', 'HEAD', 'OPTIONS', 'POST'])
        self.assert_equal(rv.data, '')

    def test_options_on_multiple_rules(self):
        app = flask.Flask(__name__)
        @app.route('/', methods=['GET', 'POST'])
        def index():
            return 'Hello World'
        @app.route('/', methods=['PUT'])
        def index_put():
            return 'Aha!'
        rv = app.test_client().open('/', method='OPTIONS')
        self.assert_equal(sorted(rv.allow), ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT'])

    def test_options_handling_disabled(self):
        app = flask.Flask(__name__)
        def index():
            return 'Hello World!'
        index.provide_automatic_options = False
        app.route('/')(index)
        rv = app.test_client().open('/', method='OPTIONS')
        self.assert_equal(rv.status_code, 405)

        app = flask.Flask(__name__)
        def index2():
            return 'Hello World!'
        index2.provide_automatic_options = True
        app.route('/', methods=['OPTIONS'])(index2)
        rv = app.test_client().open('/', method='OPTIONS')
        self.assert_equal(sorted(rv.allow), ['OPTIONS'])

    def test_request_dispatching(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return flask.request.method
        @app.route('/more', methods=['GET', 'POST'])
        def more():
            return flask.request.method

        c = app.test_client()
        self.assert_equal(c.get('/').data, 'GET')
        rv = c.post('/')
        self.assert_equal(rv.status_code, 405)
        self.assert_equal(sorted(rv.allow), ['GET', 'HEAD', 'OPTIONS'])
        rv = c.head('/')
        self.assert_equal(rv.status_code, 200)
        self.assert_(not rv.data) # head truncates
        self.assert_equal(c.post('/more').data, 'POST')
        self.assert_equal(c.get('/more').data, 'GET')
        rv = c.delete('/more')
        self.assert_equal(rv.status_code, 405)
        self.assert_equal(sorted(rv.allow), ['GET', 'HEAD', 'OPTIONS', 'POST'])

    def test_url_mapping(self):
        app = flask.Flask(__name__)
        def index():
            return flask.request.method
        def more():
            return flask.request.method

        app.add_url_rule('/', 'index', index)
        app.add_url_rule('/more', 'more', more, methods=['GET', 'POST'])

        c = app.test_client()
        self.assert_equal(c.get('/').data, 'GET')
        rv = c.post('/')
        self.assert_equal(rv.status_code, 405)
        self.assert_equal(sorted(rv.allow), ['GET', 'HEAD', 'OPTIONS'])
        rv = c.head('/')
        self.assert_equal(rv.status_code, 200)
        self.assert_(not rv.data) # head truncates
        self.assert_equal(c.post('/more').data, 'POST')
        self.assert_equal(c.get('/more').data, 'GET')
        rv = c.delete('/more')
        self.assert_equal(rv.status_code, 405)
        self.assert_equal(sorted(rv.allow), ['GET', 'HEAD', 'OPTIONS', 'POST'])

    def test_werkzeug_routing(self):
        from werkzeug.routing import Submount, Rule
        app = flask.Flask(__name__)
        app.url_map.add(Submount('/foo', [
            Rule('/bar', endpoint='bar'),
            Rule('/', endpoint='index')
        ]))
        def bar():
            return 'bar'
        def index():
            return 'index'
        app.view_functions['bar'] = bar
        app.view_functions['index'] = index

        c = app.test_client()
        self.assert_equal(c.get('/foo/').data, 'index')
        self.assert_equal(c.get('/foo/bar').data, 'bar')

    def test_endpoint_decorator(self):
        from werkzeug.routing import Submount, Rule
        app = flask.Flask(__name__)
        app.url_map.add(Submount('/foo', [
            Rule('/bar', endpoint='bar'),
            Rule('/', endpoint='index')
        ]))

        @app.endpoint('bar')
        def bar():
            return 'bar'

        @app.endpoint('index')
        def index():
            return 'index'

        c = app.test_client()
        self.assert_equal(c.get('/foo/').data, 'index')
        self.assert_equal(c.get('/foo/bar').data, 'bar')

    def test_session(self):
        app = flask.Flask(__name__)
        app.secret_key = 'testkey'
        @app.route('/set', methods=['POST'])
        def set():
            flask.session['value'] = flask.request.form['value']
            return 'value set'
        @app.route('/get')
        def get():
            return flask.session['value']

        c = app.test_client()
        self.assert_equal(c.post('/set', data={'value': '42'}).data, 'value set')
        self.assert_equal(c.get('/get').data, '42')

    def test_session_using_server_name(self):
        app = flask.Flask(__name__)
        app.config.update(
            SECRET_KEY='foo',
            SERVER_NAME='example.com'
        )
        @app.route('/')
        def index():
            flask.session['testing'] = 42
            return 'Hello World'
        rv = app.test_client().get('/', 'http://example.com/')
        self.assert_('domain=.example.com' in rv.headers['set-cookie'].lower())
        self.assert_('httponly' in rv.headers['set-cookie'].lower())

    def test_session_using_server_name_and_port(self):
        app = flask.Flask(__name__)
        app.config.update(
            SECRET_KEY='foo',
            SERVER_NAME='example.com:8080'
        )
        @app.route('/')
        def index():
            flask.session['testing'] = 42
            return 'Hello World'
        rv = app.test_client().get('/', 'http://example.com:8080/')
        self.assert_('domain=.example.com' in rv.headers['set-cookie'].lower())
        self.assert_('httponly' in rv.headers['set-cookie'].lower())

    def test_session_using_application_root(self):
        class PrefixPathMiddleware(object):
            def __init__(self, app, prefix):
                self.app = app
                self.prefix = prefix
            def __call__(self, environ, start_response):
                environ['SCRIPT_NAME'] = self.prefix
                return self.app(environ, start_response)

        app = flask.Flask(__name__)
        app.wsgi_app = PrefixPathMiddleware(app.wsgi_app, '/bar')
        app.config.update(
            SECRET_KEY='foo',
            APPLICATION_ROOT='/bar'
        )
        @app.route('/')
        def index():
            flask.session['testing'] = 42
            return 'Hello World'
        rv = app.test_client().get('/', 'http://example.com:8080/')
        self.assert_('path=/bar' in rv.headers['set-cookie'].lower())

    def test_session_using_session_settings(self):
        app = flask.Flask(__name__)
        app.config.update(
            SECRET_KEY='foo',
            SERVER_NAME='www.example.com:8080',
            APPLICATION_ROOT='/test',
            SESSION_COOKIE_DOMAIN='.example.com',
            SESSION_COOKIE_HTTPONLY=False,
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_PATH='/'
        )
        @app.route('/')
        def index():
            flask.session['testing'] = 42
            return 'Hello World'
        rv = app.test_client().get('/', 'http://www.example.com:8080/test/')
        cookie = rv.headers['set-cookie'].lower()
        self.assert_('domain=.example.com' in cookie)
        self.assert_('path=/;' in cookie)
        self.assert_('secure' in cookie)
        self.assert_('httponly' not in cookie)

    def test_missing_session(self):
        app = flask.Flask(__name__)
        def expect_exception(f, *args, **kwargs):
            try:
                f(*args, **kwargs)
            except RuntimeError, e:
                self.assert_(e.args and 'session is unavailable' in e.args[0])
            else:
                self.assert_(False, 'expected exception')
        with app.test_request_context():
            self.assert_(flask.session.get('missing_key') is None)
            expect_exception(flask.session.__setitem__, 'foo', 42)
            expect_exception(flask.session.pop, 'foo')

    def test_session_expiration(self):
        permanent = True
        app = flask.Flask(__name__)
        app.secret_key = 'testkey'
        @app.route('/')
        def index():
            flask.session['test'] = 42
            flask.session.permanent = permanent
            return ''

        @app.route('/test')
        def test():
            return unicode(flask.session.permanent)

        client = app.test_client()
        rv = client.get('/')
        self.assert_('set-cookie' in rv.headers)
        match = re.search(r'\bexpires=([^;]+)', rv.headers['set-cookie'])
        expires = parse_date(match.group())
        expected = datetime.utcnow() + app.permanent_session_lifetime
        self.assert_equal(expires.year, expected.year)
        self.assert_equal(expires.month, expected.month)
        self.assert_equal(expires.day, expected.day)

        rv = client.get('/test')
        self.assert_equal(rv.data, 'True')

        permanent = False
        rv = app.test_client().get('/')
        self.assert_('set-cookie' in rv.headers)
        match = re.search(r'\bexpires=([^;]+)', rv.headers['set-cookie'])
        self.assert_(match is None)

    def test_session_stored_last(self):
        app = flask.Flask(__name__)
        app.secret_key = 'development-key'
        app.testing = True

        @app.after_request
        def modify_session(response):
            flask.session['foo'] = 42
            return response
        @app.route('/')
        def dump_session_contents():
            return repr(flask.session.get('foo'))

        c = app.test_client()
        self.assert_equal(c.get('/').data, 'None')
        self.assert_equal(c.get('/').data, '42')

    def test_session_special_types(self):
        app = flask.Flask(__name__)
        app.secret_key = 'development-key'
        app.testing = True
        now = datetime.utcnow().replace(microsecond=0)

        @app.after_request
        def modify_session(response):
            flask.session['m'] = flask.Markup('Hello!')
            flask.session['dt'] = now
            flask.session['t'] = (1, 2, 3)
            return response

        @app.route('/')
        def dump_session_contents():
            return pickle.dumps(dict(flask.session))

        c = app.test_client()
        c.get('/')
        rv = pickle.loads(c.get('/').data)
        self.assert_equal(rv['m'], flask.Markup('Hello!'))
        self.assert_equal(type(rv['m']), flask.Markup)
        self.assert_equal(rv['dt'], now)
        self.assert_equal(rv['t'], (1, 2, 3))

    def test_flashes(self):
        app = flask.Flask(__name__)
        app.secret_key = 'testkey'

        with app.test_request_context():
            self.assert_(not flask.session.modified)
            flask.flash('Zap')
            flask.session.modified = False
            flask.flash('Zip')
            self.assert_(flask.session.modified)
            self.assert_equal(list(flask.get_flashed_messages()), ['Zap', 'Zip'])

    def test_extended_flashing(self):
        # Be sure app.testing=True below, else tests can fail silently.
        #
        # Specifically, if app.testing is not set to True, the AssertionErrors
        # in the view functions will cause a 500 response to the test client
        # instead of propagating exceptions.

        app = flask.Flask(__name__)
        app.secret_key = 'testkey'
        app.testing = True

        @app.route('/')
        def index():
            flask.flash(u'Hello World')
            flask.flash(u'Hello World', 'error')
            flask.flash(flask.Markup(u'<em>Testing</em>'), 'warning')
            return ''

        @app.route('/test/')
        def test():
            messages = flask.get_flashed_messages()
            self.assert_equal(len(messages), 3)
            self.assert_equal(messages[0], u'Hello World')
            self.assert_equal(messages[1], u'Hello World')
            self.assert_equal(messages[2], flask.Markup(u'<em>Testing</em>'))
            return ''

        @app.route('/test_with_categories/')
        def test_with_categories():
            messages = flask.get_flashed_messages(with_categories=True)
            self.assert_equal(len(messages), 3)
            self.assert_equal(messages[0], ('message', u'Hello World'))
            self.assert_equal(messages[1], ('error', u'Hello World'))
            self.assert_equal(messages[2], ('warning', flask.Markup(u'<em>Testing</em>')))
            return ''

        @app.route('/test_filter/')
        def test_filter():
            messages = flask.get_flashed_messages(category_filter=['message'], with_categories=True)
            self.assert_equal(len(messages), 1)
            self.assert_equal(messages[0], ('message', u'Hello World'))
            return ''

        @app.route('/test_filters/')
        def test_filters():
            messages = flask.get_flashed_messages(category_filter=['message', 'warning'], with_categories=True)
            self.assert_equal(len(messages), 2)
            self.assert_equal(messages[0], ('message', u'Hello World'))
            self.assert_equal(messages[1], ('warning', flask.Markup(u'<em>Testing</em>')))
            return ''

        @app.route('/test_filters_without_returning_categories/')
        def test_filters2():
            messages = flask.get_flashed_messages(category_filter=['message', 'warning'])
            self.assert_equal(len(messages), 2)
            self.assert_equal(messages[0], u'Hello World')
            self.assert_equal(messages[1], flask.Markup(u'<em>Testing</em>'))
            return ''

        # Create new test client on each test to clean flashed messages.

        c = app.test_client()
        c.get('/')
        c.get('/test/')

        c = app.test_client()
        c.get('/')
        c.get('/test_with_categories/')

        c = app.test_client()
        c.get('/')
        c.get('/test_filter/')

        c = app.test_client()
        c.get('/')
        c.get('/test_filters/')

        c = app.test_client()
        c.get('/')
        c.get('/test_filters_without_returning_categories/')

    def test_request_processing(self):
        app = flask.Flask(__name__)
        evts = []
        @app.before_request
        def before_request():
            evts.append('before')
        @app.after_request
        def after_request(response):
            response.data += '|after'
            evts.append('after')
            return response
        @app.route('/')
        def index():
            self.assert_('before' in evts)
            self.assert_('after' not in evts)
            return 'request'
        self.assert_('after' not in evts)
        rv = app.test_client().get('/').data
        self.assert_('after' in evts)
        self.assert_equal(rv, 'request|after')

    def test_after_request_processing(self):
        app = flask.Flask(__name__)
        app.testing = True
        @app.route('/')
        def index():
            @flask.after_this_request
            def foo(response):
                response.headers['X-Foo'] = 'a header'
                return response
            return 'Test'
        c = app.test_client()
        resp = c.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers['X-Foo'], 'a header')

    def test_teardown_request_handler(self):
        called = []
        app = flask.Flask(__name__)
        @app.teardown_request
        def teardown_request(exc):
            called.append(True)
            return "Ignored"
        @app.route('/')
        def root():
            return "Response"
        rv = app.test_client().get('/')
        self.assert_equal(rv.status_code, 200)
        self.assert_('Response' in rv.data)
        self.assert_equal(len(called), 1)

    def test_teardown_request_handler_debug_mode(self):
        called = []
        app = flask.Flask(__name__)
        app.testing = True
        @app.teardown_request
        def teardown_request(exc):
            called.append(True)
            return "Ignored"
        @app.route('/')
        def root():
            return "Response"
        rv = app.test_client().get('/')
        self.assert_equal(rv.status_code, 200)
        self.assert_('Response' in rv.data)
        self.assert_equal(len(called), 1)

    def test_teardown_request_handler_error(self):
        called = []
        app = flask.Flask(__name__)
        @app.teardown_request
        def teardown_request1(exc):
            self.assert_equal(type(exc), ZeroDivisionError)
            called.append(True)
            # This raises a new error and blows away sys.exc_info(), so we can
            # test that all teardown_requests get passed the same original
            # exception.
            try:
                raise TypeError
            except:
                pass
        @app.teardown_request
        def teardown_request2(exc):
            self.assert_equal(type(exc), ZeroDivisionError)
            called.append(True)
            # This raises a new error and blows away sys.exc_info(), so we can
            # test that all teardown_requests get passed the same original
            # exception.
            try:
                raise TypeError
            except:
                pass
        @app.route('/')
        def fails():
            1/0
        rv = app.test_client().get('/')
        self.assert_equal(rv.status_code, 500)
        self.assert_('Internal Server Error' in rv.data)
        self.assert_equal(len(called), 2)

    def test_before_after_request_order(self):
        called = []
        app = flask.Flask(__name__)
        @app.before_request
        def before1():
            called.append(1)
        @app.before_request
        def before2():
            called.append(2)
        @app.after_request
        def after1(response):
            called.append(4)
            return response
        @app.after_request
        def after2(response):
            called.append(3)
            return response
        @app.teardown_request
        def finish1(exc):
            called.append(6)
        @app.teardown_request
        def finish2(exc):
            called.append(5)
        @app.route('/')
        def index():
            return '42'
        rv = app.test_client().get('/')
        self.assert_equal(rv.data, '42')
        self.assert_equal(called, [1, 2, 3, 4, 5, 6])

    def test_error_handling(self):
        app = flask.Flask(__name__)
        @app.errorhandler(404)
        def not_found(e):
            return 'not found', 404
        @app.errorhandler(500)
        def internal_server_error(e):
            return 'internal server error', 500
        @app.route('/')
        def index():
            flask.abort(404)
        @app.route('/error')
        def error():
            1 // 0
        c = app.test_client()
        rv = c.get('/')
        self.assert_equal(rv.status_code, 404)
        self.assert_equal(rv.data, 'not found')
        rv = c.get('/error')
        self.assert_equal(rv.status_code, 500)
        self.assert_equal('internal server error', rv.data)

    def test_before_request_and_routing_errors(self):
        app = flask.Flask(__name__)
        @app.before_request
        def attach_something():
            flask.g.something = 'value'
        @app.errorhandler(404)
        def return_something(error):
            return flask.g.something, 404
        rv = app.test_client().get('/')
        self.assert_equal(rv.status_code, 404)
        self.assert_equal(rv.data, 'value')

    def test_user_error_handling(self):
        class MyException(Exception):
            pass

        app = flask.Flask(__name__)
        @app.errorhandler(MyException)
        def handle_my_exception(e):
            self.assert_(isinstance(e, MyException))
            return '42'
        @app.route('/')
        def index():
            raise MyException()

        c = app.test_client()
        self.assert_equal(c.get('/').data, '42')

    def test_trapping_of_bad_request_key_errors(self):
        app = flask.Flask(__name__)
        app.testing = True
        @app.route('/fail')
        def fail():
            flask.request.form['missing_key']
        c = app.test_client()
        self.assert_equal(c.get('/fail').status_code, 400)

        app.config['TRAP_BAD_REQUEST_ERRORS'] = True
        c = app.test_client()
        try:
            c.get('/fail')
        except KeyError, e:
            self.assert_(isinstance(e, BadRequest))
        else:
            self.fail('Expected exception')

    def test_trapping_of_all_http_exceptions(self):
        app = flask.Flask(__name__)
        app.testing = True
        app.config['TRAP_HTTP_EXCEPTIONS'] = True
        @app.route('/fail')
        def fail():
            flask.abort(404)

        c = app.test_client()
        try:
            c.get('/fail')
        except NotFound, e:
            pass
        else:
            self.fail('Expected exception')

    def test_enctype_debug_helper(self):
        from flask.debughelpers import DebugFilesKeyError
        app = flask.Flask(__name__)
        app.debug = True
        @app.route('/fail', methods=['POST'])
        def index():
            return flask.request.files['foo'].filename

        # with statement is important because we leave an exception on the
        # stack otherwise and we want to ensure that this is not the case
        # to not negatively affect other tests.
        with app.test_client() as c:
            try:
                c.post('/fail', data={'foo': 'index.txt'})
            except DebugFilesKeyError, e:
                self.assert_('no file contents were transmitted' in str(e))
                self.assert_('This was submitted: "index.txt"' in str(e))
            else:
                self.fail('Expected exception')

    def test_teardown_on_pop(self):
        buffer = []
        app = flask.Flask(__name__)
        @app.teardown_request
        def end_of_request(exception):
            buffer.append(exception)

        ctx = app.test_request_context()
        ctx.push()
        self.assert_equal(buffer, [])
        ctx.pop()
        self.assert_equal(buffer, [None])

    def test_response_creation(self):
        app = flask.Flask(__name__)
        @app.route('/unicode')
        def from_unicode():
            return u'Hällo Wörld'
        @app.route('/string')
        def from_string():
            return u'Hällo Wörld'.encode('utf-8')
        @app.route('/args')
        def from_tuple():
            return 'Meh', 400, {
                'X-Foo': 'Testing',
                'Content-Type': 'text/plain; charset=utf-8'
            }
        c = app.test_client()
        self.assert_equal(c.get('/unicode').data, u'Hällo Wörld'.encode('utf-8'))
        self.assert_equal(c.get('/string').data, u'Hällo Wörld'.encode('utf-8'))
        rv = c.get('/args')
        self.assert_equal(rv.data, 'Meh')
        self.assert_equal(rv.headers['X-Foo'], 'Testing')
        self.assert_equal(rv.status_code, 400)
        self.assert_equal(rv.mimetype, 'text/plain')

    def test_make_response(self):
        app = flask.Flask(__name__)
        with app.test_request_context():
            rv = flask.make_response()
            self.assert_equal(rv.status_code, 200)
            self.assert_equal(rv.data, '')
            self.assert_equal(rv.mimetype, 'text/html')

            rv = flask.make_response('Awesome')
            self.assert_equal(rv.status_code, 200)
            self.assert_equal(rv.data, 'Awesome')
            self.assert_equal(rv.mimetype, 'text/html')

            rv = flask.make_response('W00t', 404)
            self.assert_equal(rv.status_code, 404)
            self.assert_equal(rv.data, 'W00t')
            self.assert_equal(rv.mimetype, 'text/html')

    def test_make_response_with_response_instance(self):
        app = flask.Flask(__name__)
        with app.test_request_context():
            rv = flask.make_response(
                flask.jsonify({'msg': 'W00t'}), 400)
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.data,
                             '{\n  "msg": "W00t"\n}')
            self.assertEqual(rv.mimetype, 'application/json')

            rv = flask.make_response(
                flask.Response(''), 400)
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.data, '')
            self.assertEqual(rv.mimetype, 'text/html')

            rv = flask.make_response(
                flask.Response('', headers={'Content-Type': 'text/html'}),
                400, [('X-Foo', 'bar')])
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.headers['Content-Type'], 'text/html')
            self.assertEqual(rv.headers['X-Foo'], 'bar')

    def test_url_generation(self):
        app = flask.Flask(__name__)
        @app.route('/hello/<name>', methods=['POST'])
        def hello():
            pass
        with app.test_request_context():
            self.assert_equal(flask.url_for('hello', name='test x'), '/hello/test%20x')
            self.assert_equal(flask.url_for('hello', name='test x', _external=True),
                              'http://localhost/hello/test%20x')

    def test_build_error_handler(self):
        app = flask.Flask(__name__)

        # Test base case, a URL which results in a BuildError.
        with app.test_request_context():
            self.assertRaises(BuildError, flask.url_for, 'spam')

        # Verify the error is re-raised if not the current exception.
        try:
            with app.test_request_context():
                flask.url_for('spam')
        except BuildError, error:
            pass
        try:
            raise RuntimeError('Test case where BuildError is not current.')
        except RuntimeError:
            self.assertRaises(BuildError, app.handle_url_build_error, error, 'spam', {})

        # Test a custom handler.
        def handler(error, endpoint, values):
            # Just a test.
            return '/test_handler/'
        app.url_build_error_handlers.append(handler)
        with app.test_request_context():
            self.assert_equal(flask.url_for('spam'), '/test_handler/')

    def test_custom_converters(self):
        from werkzeug.routing import BaseConverter
        class ListConverter(BaseConverter):
            def to_python(self, value):
                return value.split(',')
            def to_url(self, value):
                base_to_url = super(ListConverter, self).to_url
                return ','.join(base_to_url(x) for x in value)
        app = flask.Flask(__name__)
        app.url_map.converters['list'] = ListConverter
        @app.route('/<list:args>')
        def index(args):
            return '|'.join(args)
        c = app.test_client()
        self.assert_equal(c.get('/1,2,3').data, '1|2|3')

    def test_static_files(self):
        app = flask.Flask(__name__)
        rv = app.test_client().get('/static/index.html')
        self.assert_equal(rv.status_code, 200)
        self.assert_equal(rv.data.strip(), '<h1>Hello World!</h1>')
        with app.test_request_context():
            self.assert_equal(flask.url_for('static', filename='index.html'),
                              '/static/index.html')

    def test_none_response(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def test():
            return None
        try:
            app.test_client().get('/')
        except ValueError, e:
            self.assert_equal(str(e), 'View function did not return a response')
            pass
        else:
            self.assert_("Expected ValueError")

    def test_request_locals(self):
        self.assert_equal(repr(flask.g), '<LocalProxy unbound>')
        self.assertFalse(flask.g)

    def test_proper_test_request_context(self):
        app = flask.Flask(__name__)
        app.config.update(
            SERVER_NAME='localhost.localdomain:5000'
        )

        @app.route('/')
        def index():
            return None

        @app.route('/', subdomain='foo')
        def sub():
            return None

        with app.test_request_context('/'):
            self.assert_equal(flask.url_for('index', _external=True), 'http://localhost.localdomain:5000/')

        with app.test_request_context('/'):
            self.assert_equal(flask.url_for('sub', _external=True), 'http://foo.localhost.localdomain:5000/')

        try:
            with app.test_request_context('/', environ_overrides={'HTTP_HOST': 'localhost'}):
                pass
        except Exception, e:
            self.assert_(isinstance(e, ValueError))
            self.assert_equal(str(e), "the server name provided " +
                    "('localhost.localdomain:5000') does not match the " + \
                    "server name from the WSGI environment ('localhost')")

        try:
            app.config.update(SERVER_NAME='localhost')
            with app.test_request_context('/', environ_overrides={'SERVER_NAME': 'localhost'}):
                pass
        except ValueError, e:
            raise ValueError(
                "No ValueError exception should have been raised \"%s\"" % e
            )

        try:
            app.config.update(SERVER_NAME='localhost:80')
            with app.test_request_context('/', environ_overrides={'SERVER_NAME': 'localhost:80'}):
                pass
        except ValueError, e:
            raise ValueError(
                "No ValueError exception should have been raised \"%s\"" % e
            )

    def test_test_app_proper_environ(self):
        app = flask.Flask(__name__)
        app.config.update(
            SERVER_NAME='localhost.localdomain:5000'
        )
        @app.route('/')
        def index():
            return 'Foo'

        @app.route('/', subdomain='foo')
        def subdomain():
            return 'Foo SubDomain'

        rv = app.test_client().get('/')
        self.assert_equal(rv.data, 'Foo')

        rv = app.test_client().get('/', 'http://localhost.localdomain:5000')
        self.assert_equal(rv.data, 'Foo')

        rv = app.test_client().get('/', 'https://localhost.localdomain:5000')
        self.assert_equal(rv.data, 'Foo')

        app.config.update(SERVER_NAME='localhost.localdomain')
        rv = app.test_client().get('/', 'https://localhost.localdomain')
        self.assert_equal(rv.data, 'Foo')

        try:
            app.config.update(SERVER_NAME='localhost.localdomain:443')
            rv = app.test_client().get('/', 'https://localhost.localdomain')
            # Werkzeug 0.8
            self.assert_equal(rv.status_code, 404)
        except ValueError, e:
            # Werkzeug 0.7
            self.assert_equal(str(e), "the server name provided " +
                    "('localhost.localdomain:443') does not match the " + \
                    "server name from the WSGI environment ('localhost.localdomain')")

        try:
            app.config.update(SERVER_NAME='localhost.localdomain')
            rv = app.test_client().get('/', 'http://foo.localhost')
            # Werkzeug 0.8
            self.assert_equal(rv.status_code, 404)
        except ValueError, e:
            # Werkzeug 0.7
            self.assert_equal(str(e), "the server name provided " + \
                    "('localhost.localdomain') does not match the " + \
                    "server name from the WSGI environment ('foo.localhost')")

        rv = app.test_client().get('/', 'http://foo.localhost.localdomain')
        self.assert_equal(rv.data, 'Foo SubDomain')

    def test_exception_propagation(self):
        def apprunner(configkey):
            app = flask.Flask(__name__)
            @app.route('/')
            def index():
                1/0
            c = app.test_client()
            if config_key is not None:
                app.config[config_key] = True
                try:
                    resp = c.get('/')
                except Exception:
                    pass
                else:
                    self.fail('expected exception')
            else:
                self.assert_equal(c.get('/').status_code, 500)

        # we have to run this test in an isolated thread because if the
        # debug flag is set to true and an exception happens the context is
        # not torn down.  This causes other tests that run after this fail
        # when they expect no exception on the stack.
        for config_key in 'TESTING', 'PROPAGATE_EXCEPTIONS', 'DEBUG', None:
            t = Thread(target=apprunner, args=(config_key,))
            t.start()
            t.join()

    def test_max_content_length(self):
        app = flask.Flask(__name__)
        app.config['MAX_CONTENT_LENGTH'] = 64
        @app.before_request
        def always_first():
            flask.request.form['myfile']
            self.assert_(False)
        @app.route('/accept', methods=['POST'])
        def accept_file():
            flask.request.form['myfile']
            self.assert_(False)
        @app.errorhandler(413)
        def catcher(error):
            return '42'

        c = app.test_client()
        rv = c.post('/accept', data={'myfile': 'foo' * 100})
        self.assert_equal(rv.data, '42')

    def test_url_processors(self):
        app = flask.Flask(__name__)

        @app.url_defaults
        def add_language_code(endpoint, values):
            if flask.g.lang_code is not None and \
               app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
                values.setdefault('lang_code', flask.g.lang_code)

        @app.url_value_preprocessor
        def pull_lang_code(endpoint, values):
            flask.g.lang_code = values.pop('lang_code', None)

        @app.route('/<lang_code>/')
        def index():
            return flask.url_for('about')

        @app.route('/<lang_code>/about')
        def about():
            return flask.url_for('something_else')

        @app.route('/foo')
        def something_else():
            return flask.url_for('about', lang_code='en')

        c = app.test_client()

        self.assert_equal(c.get('/de/').data, '/de/about')
        self.assert_equal(c.get('/de/about').data, '/foo')
        self.assert_equal(c.get('/foo').data, '/en/about')
        
    def test_inject_blueprint_url_defaults(self):
        app = flask.Flask(__name__)
        bp = flask.Blueprint('foo.bar.baz', __name__, 
                       template_folder='template')

        @bp.url_defaults
        def bp_defaults(endpoint, values):
            values['page'] = 'login'
        @bp.route('/<page>')
        def view(page): pass

        app.register_blueprint(bp)

        values = dict()
        app.inject_url_defaults('foo.bar.baz.view', values)
        expected = dict(page='login')
        self.assert_equal(values, expected) 

        with app.test_request_context('/somepage'):
            url = flask.url_for('foo.bar.baz.view')
        expected = '/login'
        self.assert_equal(url, expected)

    def test_debug_mode_complains_after_first_request(self):
        app = flask.Flask(__name__)
        app.debug = True
        @app.route('/')
        def index():
            return 'Awesome'
        self.assert_(not app.got_first_request)
        self.assert_equal(app.test_client().get('/').data, 'Awesome')
        try:
            @app.route('/foo')
            def broken():
                return 'Meh'
        except AssertionError, e:
            self.assert_('A setup function was called' in str(e))
        else:
            self.fail('Expected exception')

        app.debug = False
        @app.route('/foo')
        def working():
            return 'Meh'
        self.assert_equal(app.test_client().get('/foo').data, 'Meh')
        self.assert_(app.got_first_request)

    def test_before_first_request_functions(self):
        got = []
        app = flask.Flask(__name__)
        @app.before_first_request
        def foo():
            got.append(42)
        c = app.test_client()
        c.get('/')
        self.assert_equal(got, [42])
        c.get('/')
        self.assert_equal(got, [42])
        self.assert_(app.got_first_request)

    def test_routing_redirect_debugging(self):
        app = flask.Flask(__name__)
        app.debug = True
        @app.route('/foo/', methods=['GET', 'POST'])
        def foo():
            return 'success'
        with app.test_client() as c:
            try:
                c.post('/foo', data={})
            except AssertionError, e:
                self.assert_('http://localhost/foo/' in str(e))
                self.assert_('Make sure to directly send your POST-request '
                             'to this URL' in str(e))
            else:
                self.fail('Expected exception')

            rv = c.get('/foo', data={}, follow_redirects=True)
            self.assert_equal(rv.data, 'success')

        app.debug = False
        with app.test_client() as c:
            rv = c.post('/foo', data={}, follow_redirects=True)
            self.assert_equal(rv.data, 'success')

    def test_route_decorator_custom_endpoint(self):
        app = flask.Flask(__name__)
        app.debug = True

        @app.route('/foo/')
        def foo():
            return flask.request.endpoint

        @app.route('/bar/', endpoint='bar')
        def for_bar():
            return flask.request.endpoint

        @app.route('/bar/123', endpoint='123')
        def for_bar_foo():
            return flask.request.endpoint

        with app.test_request_context():
            assert flask.url_for('foo') == '/foo/'
            assert flask.url_for('bar') == '/bar/'
            assert flask.url_for('123') == '/bar/123'

        c = app.test_client()
        self.assertEqual(c.get('/foo/').data, 'foo')
        self.assertEqual(c.get('/bar/').data, 'bar')
        self.assertEqual(c.get('/bar/123').data, '123')

    def test_preserve_only_once(self):
        app = flask.Flask(__name__)
        app.debug = True

        @app.route('/fail')
        def fail_func():
            1/0

        c = app.test_client()
        for x in xrange(3):
            with self.assert_raises(ZeroDivisionError):
                c.get('/fail')

        self.assert_(flask._request_ctx_stack.top is not None)
        flask._request_ctx_stack.pop()
        self.assert_(flask._request_ctx_stack.top is None)


class ContextTestCase(FlaskTestCase):

    def test_context_binding(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return 'Hello %s!' % flask.request.args['name']
        @app.route('/meh')
        def meh():
            return flask.request.url

        with app.test_request_context('/?name=World'):
            self.assert_equal(index(), 'Hello World!')
        with app.test_request_context('/meh'):
            self.assert_equal(meh(), 'http://localhost/meh')
        self.assert_(flask._request_ctx_stack.top is None)

    def test_context_test(self):
        app = flask.Flask(__name__)
        self.assert_(not flask.request)
        self.assert_(not flask.has_request_context())
        ctx = app.test_request_context()
        ctx.push()
        try:
            self.assert_(flask.request)
            self.assert_(flask.has_request_context())
        finally:
            ctx.pop()

    def test_manual_context_binding(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return 'Hello %s!' % flask.request.args['name']

        ctx = app.test_request_context('/?name=World')
        ctx.push()
        self.assert_equal(index(), 'Hello World!')
        ctx.pop()
        try:
            index()
        except RuntimeError:
            pass
        else:
            self.assert_(0, 'expected runtime error')


class SubdomainTestCase(FlaskTestCase):

    def test_basic_support(self):
        app = flask.Flask(__name__)
        app.config['SERVER_NAME'] = 'localhost'
        @app.route('/')
        def normal_index():
            return 'normal index'
        @app.route('/', subdomain='test')
        def test_index():
            return 'test index'

        c = app.test_client()
        rv = c.get('/', 'http://localhost/')
        self.assert_equal(rv.data, 'normal index')

        rv = c.get('/', 'http://test.localhost/')
        self.assert_equal(rv.data, 'test index')

    @emits_module_deprecation_warning
    def test_module_static_path_subdomain(self):
        app = flask.Flask(__name__)
        app.config['SERVER_NAME'] = 'example.com'
        from subdomaintestmodule import mod
        app.register_module(mod)
        c = app.test_client()
        rv = c.get('/static/hello.txt', 'http://foo.example.com/')
        self.assert_equal(rv.data.strip(), 'Hello Subdomain')

    def test_subdomain_matching(self):
        app = flask.Flask(__name__)
        app.config['SERVER_NAME'] = 'localhost'
        @app.route('/', subdomain='<user>')
        def index(user):
            return 'index for %s' % user

        c = app.test_client()
        rv = c.get('/', 'http://mitsuhiko.localhost/')
        self.assert_equal(rv.data, 'index for mitsuhiko')

    def test_subdomain_matching_with_ports(self):
        app = flask.Flask(__name__)
        app.config['SERVER_NAME'] = 'localhost:3000'
        @app.route('/', subdomain='<user>')
        def index(user):
            return 'index for %s' % user

        c = app.test_client()
        rv = c.get('/', 'http://mitsuhiko.localhost:3000/')
        self.assert_equal(rv.data, 'index for mitsuhiko')

    @emits_module_deprecation_warning
    def test_module_subdomain_support(self):
        app = flask.Flask(__name__)
        mod = flask.Module(__name__, 'test', subdomain='testing')
        app.config['SERVER_NAME'] = 'localhost'

        @mod.route('/test')
        def test():
            return 'Test'

        @mod.route('/outside', subdomain='xtesting')
        def bar():
            return 'Outside'

        app.register_module(mod)

        c = app.test_client()
        rv = c.get('/test', 'http://testing.localhost/')
        self.assert_equal(rv.data, 'Test')
        rv = c.get('/outside', 'http://xtesting.localhost/')
        self.assert_equal(rv.data, 'Outside')

