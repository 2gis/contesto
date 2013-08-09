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
    "version": "0.1.0-dev",
    "install_requires": [
        "pytest",
        "selenium",
    ],
    "license": "MIT",
    "description": "",
    "long_description": "",
    "url": "https://github.com/2gis/contesto"
}

setup(**setup_args)
