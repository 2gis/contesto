# Config

Config file can contain sections:

+ [driver section](#driver-section)
+ [utils section](#utils-section)
+ [timeout section](#timeout-section)
+ [session section](#session-section)
+ [browsermobproxy section](#browsermobproxy-section)
+ [custom user section](#custom-user-section)

You can import config
```python
>>> from contesto import config
```

 You can reach every section and option with `config.<section>['<option>']`
```python
>>> from contesto import config

>>> config.add_config_file("config.ini")
>>> config.selenium['host']
'localhost'
```
WARNING! All sections are `lowercase`.

# Config management
## Adding a new config file
```python
from contesto import config

config.add_config_file("config.ini")
```

## Config stacking
Sometimes you may want to modify some rows of tests config without rewriting full config.

For example you may want to run tests locally. You already have config file `config.ini` in your VCS
```ini
[selenium]
host: your.selenium.test.server
port: 4444
browser: chrome
```

To run tests locally, you need to change `host` option. To do so without modifying `config.ini` you can create `local.config.ini` and make a change there
```ini
[selenium]
host: localhost
```

 Then you need to add both of them.

```python
from contesto import config

config.add_config_file("config.ini")
config.add_config_file("local.config.ini")
```

In the runtime the result config is going to be like this

```ini
[selenium]
host: localhost
port: 4444
browser: chrome
```

# Sections
## Driver section

Driver section is used to form `command executor` (url where tests are going to run) and `desired capabilities`.

By default Contesto is using `selenium` section.
```ini
[selenium]
host: your.selenium.test.server
port: 4444
browser: chrome
```

Driver section consists of two kind of options:
+ `host`, `port` – are `command executor` options
+ every other option – is `desired capabilities` option

### append to desired capabilities
Every option that is written in section goes to desired capabilities, except `host` and `port`:

```ini
[selenium]
host: your.selenium.test.server
port: 4444
browser: chrome
some_option: "some_value"
```

```json
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
```

### force desired capabilities
If you want to force desired capabilities to equal some dictionary, you can write it explicitly
```ini
[Selenium]
host: your.selenium.test.server
port: 4444
desired_capabilities: {
    "browserName": "chrome"
    }
```

```json
{
    "desiredCapabilities": {
        "browserName": "chrome"
    }
}
```

### use another driver section
By default Contesto is using `selenium` driver with standard selenium bindings.
To change this behaviour you should use [DriverMixin](docs/driver_mixin.md) when creating a test case.

## Utils section
TODO
## Timeout section
TODO
## Session section
TODO
## Browsermobproxy section
TODO
## Custom user section
TODO