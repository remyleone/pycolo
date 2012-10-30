.. _api:

API
===

.. automodule:: pycolo

This part of the documentation covers all the interfaces of Pycolo.  For
parts where Pycolo depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


Main Interface
--------------

All of Request's functionality can be accessed by these 7 methods.
They all return an instance of the :class:`Response <Response>` object.


Utilities
---------

These functions are used internally, but may be useful outside of
Requests.

.. module:: structures

Status Code Lookup
~~~~~~~~~~~~~~~~~~

.. automodule:: pycolo.codes

Internals
---------

These items are an internal component to Pycolo, and should never be
seen by the end user (developer). This part of the API documentation
exists for those who are extending the functionality of Pycolo.
