This part of the documentation is related to the test performed during
the ETSI CTI Plugtests for CoAP protocol.

The goal of interoperability test is to check that devices resulting from
protocol implementations are able to work together and provide the
features provided by the protocols.

The test descriptions are provided in proforma tables. The following different types of test operator actions are considered during the test execution:
    - A *stimulus* corresponds to an event that enforces an EUT to proceed with a specific protocol action, like sending a message for instance
    - A *verify* consists of verifying that the EUT behaves according to the expected behaviour (for instance the EUT behaviour shows that it receives the expected message)
    - A *configure* corresponds to an action to modify the EUT configuration
    - A *check* ensures the correctness of protocol messages on reference points, with valid content according to the specific interoperability test purpose to be verified.


etsi Package
============

:mod:`etsi` Package
-------------------

.. automodule:: tests.etsi.__init__
    :members:
    :undoc-members:
    :show-inheritance:


Mandatory Tests
---------------

:mod:`TestCore` Module
----------------------

.. automodule:: tests.etsi.TestCore
    :members:
    :undoc-members:
    :show-inheritance:


Optional Tests
--------------

:mod:`TestBlock` Module
-----------------------

.. automodule:: tests.etsi.TestBlock
    :members:
    :undoc-members:
    :show-inheritance:


:mod:`TestLink` Module
----------------------

.. automodule:: tests.etsi.TestLink
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`TestObserve` Module
-------------------------

.. automodule:: tests.etsi.TestObserve
    :members:
    :undoc-members:
    :show-inheritance:


CoAP Binding for M2M REST Resources
-----------------------------------

TODO

Automatic testing
-----------------

:mod:`irisa` Module
-------------------

.. automodule:: tests.etsi.irisa
    :members:
    :undoc-members:
    :show-inheritance:
