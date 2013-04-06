django-formtags
===============

django-formtags is a django template library that allows you to customize
form fields directly from your templates.

Installation
------------

.. code-block:: bash

    pip install django-formtags


Documentation
-------------

You can find the latest documentation at
https://django-formtags.readthedocs.org/en/latest/


Contributing
------------

To report an issue, use the bug tracker on Github.

Pull requests are welcome.


Running the test suite
----------------------

Start by installing the requirements:

.. code-block:: bash

    pip install -r requirements_dev.txt


After that, you'll need to install a version of django.
The simplest way to do so is with pip too:

.. code-block:: bash

    pip install django


Once that's done, you can run the tests with:

.. code-block:: bash

    py.test --cov=multiform --cov-report=html tests/


Building the documentation
--------------------------

To build the documentation, go in the ``docs/`` directory and simply run
``make html``.
