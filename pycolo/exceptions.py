# coding=utf-8

"""
pycolo.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Pycolo' exceptions.

"""


class RequestException(RuntimeError):
    """There was an ambiguous exception that occurred while handling your
    request."""


class COAPError(RequestException):
    """An CoAP error occurred."""
    response = None


class ConnectionError(RequestException):
    """A Connection error occurred."""


class Timeout(RequestException):
    """The request timed out."""


class URLRequired(RequestException):
    """A valid URL is required to make a request."""


class TooManyRedirects(RequestException):
    """Too many redirects."""


class MissingSchema(RequestException, ValueError):
    """The URL schema (e.g. http or https) is missing."""


class InvalidSchema(RequestException, ValueError):
    """See defaults.py for valid schemas."""


class InvalidURL(RequestException, ValueError):
    """ The URL provided was somehow invalid. """
