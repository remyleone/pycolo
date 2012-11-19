.. _install:

Installation
============

This part of the documentation covers the installation of Pycolo.
The first step to using any software package is getting it properly installed.


Distribute & Pip
----------------

Installing pycolo is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install pycolo

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install pycolo

But, you really `shouldn't do that <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.



Get the Code
------------

Pycolo is actively developed on GitHub, where the code is
`always available <https://github.com/sieben/pycolo>`_.

You can either clone the public repository::

    git clone git://github.com/sieben/pycolo.git

Download the `tarball <https://github.com/sieben/pycolo/tarball/master>`_::

    $ curl -OL https://github.com/sieben/pycolo/tarball/master

Or, download the `zipball <https://github.com/sieben/pycolo/zipball/master>`_::

    $ curl -OL https://github.com/sieben/pycolo/zipball/master


Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install