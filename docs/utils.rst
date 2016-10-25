Utils
*****

Screenshot
==========

.. automodule:: contesto.utils.screenshot


.. autofunction:: make_screenshot

Save screenshot on error
++++++++++++++++++++++++

.. autofunction:: save_screenshot_on_error

.. autoclass:: SaveScreenshotOnError
    :members:
    :undoc-members:

Screencast
==========


Install ffmpeg::

    sudo add-apt-repository --yes ppa:mc3man/trusty-media
    sudo apt-get update
    sudo apt-get install -y ffmpeg

Install stf-utils::

    pip install git+https://github.com/2gis/stf-utils.git

Record screencast
+++++++++++++++++

.. automodule:: contesto.utils.screencast


.. autofunction:: start_screencast_recorder

.. autofunction:: stop_screencast_recorder

.. autofunction:: try_to_attach_screencast_to_results

