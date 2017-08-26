
===================================
aionap - Python Asyncio REST Client
===================================

.. image:: https://img.shields.io/pypi/v/aionap.svg
    :target: https://pypi.python.org/pypi/aionap
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/chassing/aionap.svg?branch=master
   :target: https://travis-ci.org/chassing/aionap
   :alt: Latest Travis CI build status


aionap is a Python_ asyncio enabled REST client. It uses a similar API like slumber_ and copies shameless other parts of it.

Feel free to contribute via pull requests, issues or email messages.


QuickStart
==========

1. Install aionap::

    $ pip install aionap

2. Install Optional Requirement::

    pip install pyyaml

3. Use it!


Usage
-----

* Get an API object

.. code-block:: python

    import aionap
    api = aionap.API('https://demo.api-platform.com')


* Fetch a url/resource (e.g. https://demo.api-platform.com/books)

.. code-block:: python

    async with api.books as resource:
        response = await resource.get()

For more see the documenation_, the `test/test_demo_api.py` file or the `example` directory.


Installation
------------

aionap is available via PyPI, just install it as usual.

.. code-block:: shell

    $ pip install aionap

``aionap`` requires Python >= 3.6.

**[OPTIONAL]** PyYaml (Required for the yaml serializer):

.. code-block:: shell

    $ pip install pyyaml


Features
--------

* Basic Auth support
* JSON, YAML serializers
* GET, POST, PUT, PATCH, DELETE of resources
* Good test coverage


TODO
----

* OAuth support
* Readthedocs API documenation


Compatibility
-------------

Python >= 3.6


Licence
-------

BSD 2-Clause License


Authors and Contributors
------------------------

* `Christian Assing <chris@ca-net.org>`_ (Main author)


.. _Python: http://www.python.org/
.. _slumber: https://github.com/samgiles/slumber
.. _documenation: https://xxx
