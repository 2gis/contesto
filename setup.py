from setuptools import setup, find_packages

setup_args = {
    "name": "contesto",
    "maintainer": "2GIS",
    "maintainer_email": "autoqa@2gis.ru",
    "packages": find_packages(),
    "package_data": {
        'contesto': [
            'config/*.ini'
        ],
    },
    "version": "0.2.0",
    "install_requires": [
        "selenium==2.48.0",
        "Appium-Python-Client==0.20",
        "browsermob-proxy==0.7.1"
    ],
    "license": "MIT",
    "description": "",
    "long_description": "",
    "url": "https://github.com/2gis/contesto"
}

setup(**setup_args)
