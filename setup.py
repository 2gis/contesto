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
    "version": "0.2.2",
    "install_requires": [
        "selenium==2.52.0",
        "Appium-Python-Client==0.20",
        "browsermob-proxy==0.7.1",
        "werkzeug==0.11.4",
        "stf-utils==0.0.1",
    ],
    "dependency_links": [
        "git+https://github.com/2gis/stf-utils.git@a9e85eeea8003673b200e9706a6a3ce079ddb7ca#egg=stf-utils-0.0.1"
    ],
    "license": "MIT",
    "description": "",
    "long_description": "",
    "url": "https://github.com/2gis/contesto"
}

setup(**setup_args)
