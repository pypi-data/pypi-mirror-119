# Parallely - Parallel Python made simple

[![pypi](https://img.shields.io/pypi/v/parallely.svg)](https://pypi.org/project/parallely/)
[![license](https://img.shields.io/pypi/l/parallely.svg)](https://github.com/mvilstrup/parallely/blob/main/LICENSE)
[![wheel](https://img.shields.io/pypi/wheel/parallely.svg)](https://pypi.org/project/parallely/)
[![python](https://img.shields.io/pypi/pyversions/parallely.svg)](https://pypi.org/project/parallely/)
[![Test Suite](https://github.com/mvilstrup/parallely/workflows/Test%20Suite/badge.svg)](https://github.com/mvilstrup/parallely/actions?query=workflow%3A%22Test+Suite%22)
[![Coverage Status](https://coveralls.io/repos/github/MVilstrup/parallely/badge.svg?branch=main)](https://coveralls.io/github/MVilstrup/parallely?branch=main)
[![docs](https://readthedocs.org/projects/parallely/badge/?version=latest)](https://parallely.readthedocs.io/en/latest/?badge=latest)


# Installation
`pip install paralelly`

# Multi Threading

```python
from parallely import threaded
import requests

@threaded(max_workers=500)
def fetch_data(url):
    return requests.get(url).json()

# Use the function as usual for fine grained control, testing etc. 
fetch_data("http://www.SOME-WEBSITE.com/data/cool-stuff")

# Use a thread-pool to map over a list of inputs in concurrent manner
fetch_data.map([
    "http://www.SOME-WEBSITE.com/data/cool-stuff",
    "http://www.SOME-WEBSITE.com/data/cool-stuff",
    "http://www.SOME-WEBSITE.com/data/cool-stuff"
])
```

```python
from parallely import threaded
import requests

@threaded
def fetch(min_val=100, max_val=1000, count=5):
    return requests.get(f"http://www.randomnumberapi.com/api/v1.0/random?min={min_val}&max={max_val}&count={count}").json()

fetch.map(count=list(range(10)))
```

# Multi Processing

# Asynchronous
