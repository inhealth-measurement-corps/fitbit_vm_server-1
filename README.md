Requirements
============

* Python 2.7+
* `python-dateutil`_ (always)
* `requests-oauthlib`_ (always)
* `Sphinx`_ (to create the documention)
* `tox`_ (for running the tests)
* `coverage`_ (to create test coverage reports)

.. _python-dateutil: https://pypi.python.org/pypi/python-dateutil/2.4.0
.. _requests-oauthlib: https://pypi.python.org/pypi/requests-oauthlib
.. _Sphinx: https://pypi.python.org/pypi/Sphinx
.. _tox: https://pypi.python.org/pypi/tox
.. _coverage: https://pypi.python.org/pypi/coverage/

To use the library, you need to install the run time requirements:

   sudo pip install -r requirements/base.txt

To modify and test the library, you need to install the developer requirements:

   sudo pip install -r requirements/dev.txt

To run the library on a continuous integration server, you need to install the test requirements:

   sudo pip install -r requirements/test.txt
