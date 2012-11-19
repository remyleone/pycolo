.. _quickstart:

Quickstart
==========

Eager to get started? This page gives a good introduction in how to get started
with Pycolo. This assumes you already have Pycolo installed. If you do not,
head over to the :ref:`Installation <install>` section.

First, make sure that:

* Pycolo is :ref:`installed <install>`
* Pycolo is :ref:`up-to-date <updates>`

Let's get started with some simple examples.

Make a Request
------------------

Making a request with pycolo is very simple.

Begin by importing the pycolo module::

    >>> import pycolo

Now, let's try to get a coap/.well-known. For this example, let's get GitHub's public
timeline ::

    >>> r = pycolo.get('coap://coap.sieben.fr/.well-known')

Now, we have a :class:`Response` object called ``r``. We can get all the
information we need from this object.

Pycolo simple API means that all forms of CoAP request are as obvious. For
example, this is how you make an CoAP POST request::

    >>> r = pycolo.post("coap://coap.sieben.fr/post")

Nice, right? What about the other CoAP request types: PUT, DELETE, HEAD and
OPTIONS? These are all just as simple::

    >>> r = pycolo.put("coap://coap.sieben.fr/put")
    >>> r = pycolo.delete("coap://coap.sieben.fr/delete")
    >>> r = pycolo.head("coap://coap.sieben.fr/.well-known")
    >>> r = pycolo.options("coap://coap.sieben.fr/.well-known")

That's all well and good, but it's also only the start of what Pycolo can do.


Passing Parameters In URLs
--------------------------

You often want to send some sort of data in the URL's query string. If you were
constructing the URL by hand, this data would be given as key/value pairs in
the URL after a question mark, e.g. ``coap.sieben.fr/.well-known?key=val``.  Pycolo
allows you to provide these arguments as a dictionary, using the ``params``
keyword argument. As an example, if you wanted to pass ``key1=value1`` and
``key2=value2`` to ``coap.sieben.fr/.well-known``, you would use the following code::

    >>> payload = {'key1': 'value1', 'key2': 'value2'}
    >>> r = pycolo.get("coap://coap.sieben.fr/.well-known", params=payload)

You can see that the URL has been correctly encoded by printing the URL::

    >>> print r.url
    u'coap://coap.sieben.fr/.well-known?key2=value2&key1=value1'


Response Content
----------------

We can read the content of the server's response.::

    >>> import pycolo
    >>> r = pycolo.get('coap://coap.sieben.fr/.well-known')
    >>> r.text
    '[{"resources":{"temp":42,"url":"coap://coap.sieben.fr/...

Pycolo will automatically decode content from the server. Most unicode
charsets are seamlessly decoded.

When you make a request, Pycolo makes educated guesses about the encoding of
the response based on the CoAP headers. The text encoding guessed by Pycolo
is used when you access ``r.text``. You can find out what encoding Pycolo is
using, and change it, using the ``r.encoding`` property::

    >>> r.encoding
    'utf-8'
    >>> r.encoding = 'ISO-8859-1'

If you change the encoding, Pycolo will use the new value of ``r.encoding``
whenever you call ``r.text``.

Pycolo will also use custom encodings in the event that you need them. If
you have created your own encoding and registered it with the ``codecs``
module, you can simply use the codec name as the value of ``r.encoding`` and
Pycolo will handle the decoding for you.

Binary Response Content
-----------------------

You can also access the response body as bytes, for non-text requests::

    >>> r.content
    b'[{"resources":{"temp":42,"url":"coap://coap.sieben.fr/...

The ``gzip`` and ``deflate`` transfer-encodings are automatically decoded for you.

For example, to create an image from binary data returned by a request, you can
use the following code:

    >>> from PIL import Image
    >>> from StringIO import StringIO
    >>> i = Image.open(StringIO(r.content))


JSON Response Content
---------------------

There's also a builtin JSON decoder, in case you're dealing with JSON data::

    >>> import pycolo
    >>> r = pycolo.get('coap://coap.sieben.fr/.well-known.json')
    >>> r.json
    [{u'repository': {u'open_issues': 0, u'url': 'coap://coap.sieben.fr/...

In case the JSON decoding fails, ``r.json`` simply returns ``None``.


Raw Response Content
--------------------

In the rare case that you'd like to get the absolute raw socket response from
the server, you can access ``r.raw``::

    >>> r.raw.read(10)
    '\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03'


Custom Headers
--------------

If you'd like to add CoAP headers to a request, simply pass in a ``dict`` to
the ``headers`` parameter.

For example, we didn't specify our content-type in the previous example::

    >>> import json
    >>> url = 'coap://coap.sieben.fr/some/endpoint'
    >>> payload = {'some': 'data'}
    >>> headers = {'content-type': 'application/json'}

    >>> r = pycolo.post(url, data=json.dumps(payload), headers=headers)


More complicated POST requests
------------------------------

Typically, you want to send some form-encoded data — much like an HTML form.
To do this, simply pass a dictionary to the `data` argument. Your dictionary of
data will automatically be form-encoded when the request is made::

    >>> payload = {'key1': 'value1', 'key2': 'value2'}
    >>> r = pycolo.post("coap://coap.sieben.fr/post", data=payload)
    >>> print r.text
    {
      // ...snip... //
      "form": {
        "key2": "value2",
        "key1": "value1"
      },
      // ...snip... //
    }

There are many times that you want to send data that is not form-encoded. If
you pass in a ``string`` instead of a ``dict``, that data will be posted
directly.

For example, the GitHub API v3 accepts JSON-Encoded POST/PATCH data::

    >>> import json
    >>> url = 'coap://coap.sieben.fr/some/endpoint'
    >>> payload = {'some': 'data'}

    >>> r = pycolo.post(url, data=json.dumps(payload))


POST a Multipart-Encoded File
-----------------------------

Pycolo makes it simple to upload Multipart-encoded files::

    >>> url = 'coap://coap.sieben.fr/post'
    >>> files = {'file': open('report.csv', 'rb')}

    >>> r = pycolo.post(url, files=files)
    >>> r.text
    {
      // ...snip... //
      "files": {
        "file": "<censored...binary...data>"
      },
      // ...snip... //
    }

You can set the filename explicitly::

    >>> url = 'coap://coap.sieben.fr/post'
    >>> files = {'file': ('report.csv', open('report.csv', 'rb'))}

    >>> r = pycolo.post(url, files=files)
    >>> r.text
    {
      // ...snip... //
      "files": {
        "file": "<censored...binary...data>"
      },
      // ...snip... //
    }

If you want, you can send strings to be received as files::

    >>> url = 'coap://coap.sieben.fr/post'
    >>> files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}

    >>> r = pycolo.post(url, files=files)
    >>> r.text
    {
      // ...snip... //
      "files": {
        "file": "some,data,to,send\\nanother,row,to,send\\n"
      },
      // ...snip... //
    }


Response Status Codes
---------------------

We can check the response status code::

    >>> r = pycolo.get('coap://coap.sieben.fr/.well-known')
    >>> r.status_code
    200

Pycolo also comes with a built-in status code lookup object for easy
reference::

    >>> r.status_code == pycolo.codes.ok
    True

If we made a bad request (non-200 response), we can raise it with
:class:`Response.raise_for_status()`::

    >>> bad_r = pycolo.get('coap://coap.sieben.fr/status/404')
    >>> bad_r.status_code
    404

    >>> bad_r.raise_for_status()
    Traceback (most recent call last):
        raise coap_error
    pycolo.exceptions.COAPError: 404 Client Error

But, since our ``status_code`` for ``r`` was ``200``, when we call
``raise_for_status()`` we get::

    >>> r.raise_for_status()
    None

All is well.


Response Headers
----------------

We can view the server's response headers using a Python dictionary::

    >>> r.headers
    {
        'status': '200 OK',
        'content-encoding': 'text',
        'transfer-encoding': 'chunked',
        'connection': 'close',
        'server': 'contiki/Erbium',
        'x-runtime': '148ms',
        'etag': '"e1ca502697e5c9317743dc078f67693f"',
        'content-type': 'application/json; charset=utf-8'
    }

The dictionary is special, though: it's made just for CoAP headers, CoAP
headers are case-insensitive.

So, we can access the headers using any capitalization we want::

    >>> r.headers['Content-Type']
    'application/json; charset=utf-8'

    >>> r.headers.get('content-type')
    'application/json; charset=utf-8'

If a header doesn't exist in the Response, its value defaults to ``None``::

    >>> r.headers['X-Random']
    None

Timeouts
--------

You can tell pycolo to stop waiting for a response after a given number of
seconds with the ``timeout`` parameter::

    >>> pycolo.get('coap://coap.sieben.fr/.well-known', timeout=0.001)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    pycolo.exceptions.Timeout: Request timed out.

.. admonition:: Note:

    ``timeout`` only effects the connection process itself, not the
    downloading of the response body.
