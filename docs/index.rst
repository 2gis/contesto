Welcome to Contesto's documentation!
====================================

Installation
============

::

    pip install -U git+https://github.com/2gis/contesto.git#egg=contesto

Quick start
===========

1. `download selenium-server-standalone <http://www.seleniumhq.org/download/>`_
2. run it::

    java -jar selenium-server-standalone-x.x.x.jar
3. run test::

    from contesto import ContestoTestCase

    class TestExample(ContestoTestCase):
        def test_example(self):
            self.driver.get("http://google.com")

Simple configuration
====================

In case you need some customization, for example, you prefer to run selenium server on port `9000` and you need to run tests using `chrome`

* create ``config.ini``::

    [Selenium]
    host: localhost
    port: 9000
    browserName: chrome

* add ``config.ini`` in test::

    from contesto import ContestoTestCase, config

    config.add_config_file("config.ini")

    class TestExample(ContestoTestCase):
        def test_example(self):
            self.driver.get("http://google.com")

Contents:
=========

.. toctree::
   :maxdepth: 2

   config
   page_object
   page
   component
   driver
   driver_mixin
   element
   finder
   utils
