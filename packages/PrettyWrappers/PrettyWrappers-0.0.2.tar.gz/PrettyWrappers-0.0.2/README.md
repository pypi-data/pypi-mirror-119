# Pretty Wrappers

![PyPI](https://img.shields.io/pypi/v/PrettyWrappers) ![Python 3.8, 3.9, 3.10](https://img.shields.io/pypi/pyversions/PrettyWrappers) ![License](https://img.shields.io/pypi/l/PrettyWrappers)


**Pretty Wrappers** - this module is a Python client library that adds useful for development decorators


## Installation

Install the current version with [PyPI](https://pypi.org/project/PrettyWrappers/):

```bash
pip install PrettyWrappers
```


## Usage

You can import each module individually

```python
from PrettyWrappers import timer, logging, ...
```

Or if you need to use several modules at once, you can import all library as pw

```python
import PrettyWrappers

pw = PrettyWrappers
```


## Example

---

**Timer** - Execution time counting decorator. Print the result to the console.

```python
from PrettyWrappers import timer


@timer
def request(url):
    import requests

    res = requests.get(url)
    return res


request('http://google.com')

```

*Output:*
```bash
[*] Execution time: 0.577 sec
```

---

If you need to get the execution time as a variable, for subsequent actions with it, you can use naked_timer

**Naked Timer** - Execution time counting decorator. But it returns dictionary.  

*{'execution time': float, 'result': any}*

```python
from PrettyWrappers import naked_timer


@naked_timer
def request(url):
    import requests

    res = requests.get(url)
    return res


print(request('http://google.com'))
```

*Output:*
```bash
{'execution_time': 0.589, 'result': <Response [200]>}
```

We can extract the execution time of the dictionary

```python
result = request('http://google.com')

execution_time = result['execution_time']

print(execution_time)
print(type(execution_time))
```

*Output:*
```bash
0.578
<class 'float'>
```

---

**Pause** - Pause-creating decorator.  

*@pause(seconds: int or float)*

```python
from PrettyWrappers import timer, pause


@timer
@pause(1)
def request(url):
    import requests

    res = requests.get(url)
    return res


request('http://google.com')
```

*Output without "pause" :*
```bash
[*] Execution time: 0.405 sec
```

*Output with "pause" :*
```bash
[*] Execution time: 1.405 sec
```

---

**Counter** - Decorator counting the count of calls function. Print the result to the console.

```python
from PrettyWrappers import counter


@counter
def request(url):
    import requests

    res = requests.get(url)
    return res


request('http://google.com')
request('http://pypi.org')
```

*Output:*
```bash
[*] Function [request] was called: 1x
[*] Function [request] was called: 2x
```

---

**Logging** - Logging decorator.  

(Just print information about the called function. Real logging will be added later).

```python
from PrettyWrappers import logging


@logging
def request(url):
    import requests

    res = requests.get(url)
    return res


request('http://google.com')
```

*Output:*
```bash
[*] Function: request 
 (*) args: ('http://google.com',) 
 (*) kwargs: {}
```

---

## Contributing

Bug reports and/or pull requests are welcome.

Also you can write to me  
[Instagram](https://www.instagram.com/nikitun.kun/) : @nikitun.kun


## License

The module is available as open source under the terms of the [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0)
