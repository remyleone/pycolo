.. pycolo documentation master file, created by
   sphinx-quickstart on Thu Sep  6 20:36:11 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pycolo's documentation!
==================================

Contents:

.. toctree::
   :maxdepth: 4

   pycolo


Main advice: Do not distribute state over multiple layers. CoAP unfortunately
has many cross-layer dependencies if you divide processing in more than the
Message and Req/Res layers. Especially observe is critical here. I am going to
introduce Exchange objects in Cf, which will contain all relevant information
for a request/response pair in one place. These will be passed through the
stack, which will become a pure processing pipeline then.
 
Another thing that often causes headaches is client/server symmetry in the
stack. It might be easier to follow HTTP here and have a dedicated stack for
client behavior and for server behavior. I prefer, however, to have all
block-related code for instance in a single place, i.e., layer. Thus, I will
stick to the symmetric design.
 
The last issue I can think of is multi-threading. If you want to include
cross-proxy functionality, check out the Python libraries first, e.g., for
HTTP. They often come with their own thread pools which can make your own
worker thread design quite ugly… Plan from the beginning where to dispatch,
etc.

API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Test documentation
------------------

If you are looking for information about tests and certifications and/or resources used,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   tests

Developer Guide
---------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 1

   dev/internals
   dev/todo
   dev/authors

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

