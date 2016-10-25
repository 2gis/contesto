# Contesto

[![Build Status](https://travis-ci.org/2gis/contesto.svg?branch=master)](https://travis-ci.org/2gis/contesto)

## Features

TODO

## Installation
```bash
pip install -U git+https://github.com/2gis/contesto.git#egg=contesto
```

## Quick start

1. download [selenium-server-standalone](http://www.seleniumhq.org/download/)
2. run it
```bash
java -jar selenium-server-standalone-2.45.0.jar
```
3. run test
```python
from contesto import ContestoTestCase

class TestExample(ContestoTestCase):
    def test_example(self):
        self.driver.get("http://google.com")
```

## Simple configuration

In case you need some customization, for example, you prefer to run selenium server on port `9000` and you need to run tests using `chrome`
+ create `config.ini`
```ini
[Selenium]
host: localhost
port: 9000
browserName: chrome
```
+ add `config.ini` in test
```python
from contesto import ContestoTestCase, config

config.add_config_file("config.ini")

class TestExample(ContestoTestCase):
    def test_example(self):
        self.driver.get("http://google.com")
```

## Documentation

More [information](http://contesto.readthedocs.org/)
