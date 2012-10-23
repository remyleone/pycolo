.. _api:

API
===

.. module:: pycolo

This part of the documentation covers all the interfaces of Pycolo.  For
parts where Pycolo depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


Main Interface
--------------

All of Request's functionality can be accessed by these 7 methods.
They all return an instance of the :class:`Response <Response>` object.

.. autofunction:: request

---------------------


.. autoclass:: Response
   :inherited-members:

---------------------

.. autofunction:: head
.. autofunction:: get
.. autofunction:: post
.. autofunction:: put
.. autofunction:: patch
.. autofunction:: delete

Utilities
---------

These functions are used internally, but may be useful outside of
Requests.

.. module:: pycolo.structure

Status Code Lookup
~~~~~~~~~~~~~~~~~~

.. autofunction:: pycolo.codes

::

    >>> pycolo.codes['temporary_redirect']
    307

    >>> pycolo.codes['\o/']
    200

Encodings
~~~~~~~~~

.. autofunction:: get_encodings_from_content
.. autofunction:: get_encoding_from_headers
.. autofunction:: get_unicode_from_response
.. autofunction:: decode_gzip


Internals
---------

These items are an internal component to Pycolo, and should never be
seen by the end user (developer). This part of the API documentation
exists for those who are extending the functionality of Pycolo.


Classes
~~~~~~~

.. autoclass:: pycolo.Response
   :inherited-members:

.. autoclass:: pycolo.request
   :inherited-members:
