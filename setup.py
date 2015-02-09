from setuptools import setup

setup_args = {
    "name": "contesto",
    "maintainer": "2GIS",
    "maintainer_email": "autoqa@2gis.ru",
    "packages": [
        "contesto",
        "contesto.basis",
        "contesto.core",
        "contesto.utils",
    ],
    "package_data": {
        'contesto': [
            'config/*.ini'
        ],
    },
    "version": "0.2.0",
    "install_requires": [
        "selenium==2.44.0",
        "Appium-Python-Client==0.13",
        "browsermob-proxy==0.6.0"
    ],
    "license": "MIT",
    "description": "",
    "long_description": "",
    "url": "https://github.com/2gis/contesto"
}

setup(**setup_args)
