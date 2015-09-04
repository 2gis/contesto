Config
******

Basics
======

You can import config::

    >>> from contesto import config

You can reach every section and option with ``config.section[option]``::

    >>> config.selenium['host']
    'localhost'

.. warning:: All sections are in ``lowercase``.

Adding a new config file
========================

::

    from contesto import config

    config.add_config_file("config.ini")


Config stacking
===============

Sometimes you may want to modify some rows of tests config without rewriting full config.

For example you may want to run tests locally. You already have config file ``config.ini`` in your VCS::

    [selenium]
    host: your.selenium.test.server
    port: 4444
    browser: chrome

To run tests locally, you need to change ``host`` option.

To do so without modifying ``config.ini`` you can create ``local.config.ini`` and make a change there::

    [selenium]
    host: localhost

Then you need to add both of them::

    from contesto import config

    config.add_config_file("config.ini")
    config.add_config_file("local.config.ini")

In the runtime the result config is going to be like this::

    [selenium]
    host: localhost
    port: 4444
    browser: chrome

Sections
========

Driver section
--------------

Driver section is used to form ``command executor`` (url where tests are going to run) and ``desired capabilities``.

By default Contesto is using ``selenium`` section::

    [selenium]
    host: your.selenium.test.server
    port: 4444
    browser: chrome

Driver section consists of two kind of options:

* ``host``, ``port`` – are ``command executor`` options.
* Every other option – is ``desired capabilities`` option.

append to desired capabilities
++++++++++++++++++++++++++++++

Every option that is written in section goes to desired capabilities, except ``host`` and ``port``::

    [selenium]
    host: your.selenium.test.server
    port: 4444
    browser: chrome
    some_option: "some_value"


::

    {
        "desiredCapabilities": {
            "javascriptEnabled": true,
            "platform": "ANY",
            "browserName": "chrome",
            "version": "",
            "browser": "chrome",
            "some_option": "some_value"
        }
    }

force desired capabilities
++++++++++++++++++++++++++

If you want to force desired capabilities to equal some dictionary, you can write it explicitly::

    [Selenium]
    host: your.selenium.test.server
    port: 4444
    desired_capabilities: {
        "browserName": "chrome"
        }

::

    {
        "desiredCapabilities": {
            "browserName": "chrome"
        }
    }

use another driver section
++++++++++++++++++++++++++

By default Contesto is using ``selenium`` driver with standard selenium bindings.

.. To change this behaviour you should use [DriverMixin](/driver_mixin) when creating a test case.

Utils section
-------------
- ``save_screenshots`` - if set and test method is decorated with :func:`contesto.utils.screenshot.save_screenshot_on_error` then screenshots will be saved on any uncaught exception raised in test method.
- ``screenshots_path`` - path for existing folder where screenshots will be saved (absolute or relative to current working directory).
::

    [utils]
    save_screenshots: True
    screenshot_path: /some/existing/path/screenshots/

Timeout section
---------------
TODO

Session section
---------------
TODO

Browsermobproxy section
-----------------------
TODO

Custom user section
-------------------
TODO

