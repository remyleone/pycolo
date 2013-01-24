# coding=utf-8

"""
pycolo.api

This module implements the "requests" Pycolo API
"""
from . import sessions

def request(method, url, **kwargs):
    """
    Constructs and sends a :class:`Request <Request>`.
    Returns :class:`Response <Response>` object.

    :param method: method for the new :class:`Request` object.
    :param url: URL for the new :class:`Request` object.

    :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
    :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of CoAP Headers to send with the :class:`Request`.
    :param files: (optional) Dictionary of 'name': file-like-objects (or {'name': ('filename', fileobj)}) for multipart encoding upload.
    :param timeout: (optional) Float describing the timeout of the request.
    :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param return_response: (optional) If False, an un-sent Request object will returned.
    :param session: (optional) A :class:`Session` object to be used for the request.
    :param config: (optional) A configuration dictionary. See ``request.defaults`` for allowed keys and their default values.
    :param prefetch: (optional) if ``True``, the response content will be immediately downloaded.

    Usage::

      >>> import requests
      >>> req = requests.request('GET', 'http://httpbin.org/get')
      <Response [200]>
    """
    session = sessions.Session()
    return session.request(method=method, url=url, **kwargs)


def get(url, **kwargs):
    """Sends a GET request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """

    kwargs.setdefault('allow_redirects', True)
    return request('get', url, **kwargs)

def observe(url, **kwargs):
    """
    Sends a OBSERVATION request.
    Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """
    return request("observe", url, **kwargs)

def post(url, data=None, **kwargs):
    """
    Sends a POST request.
    Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """

    return request('post', url, data=data, **kwargs)


def put(url, data=None, **kwargs):
    """
    Sends a PUT request.
    Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """
    return request('put', url, data=data, **kwargs)


def delete(url, **kwargs):
    """
    Sends a DELETE request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """
    return request('delete', url, **kwargs)
