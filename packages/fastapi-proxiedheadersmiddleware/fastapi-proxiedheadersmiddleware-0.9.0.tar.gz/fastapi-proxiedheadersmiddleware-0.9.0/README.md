# HTTP Proxy Header support for FastAPI

This Python package allows transparent use of FastAPI-based solutions behind
proxies which set `X-Forwarded-...` headers. Applications will construct URLs
based on those headers rather than the incoming `Host` header.

## Use

Install `fastapi-proxiedheadersmiddleware` using pip:

```
pip install fastapi-proxiedheadersmiddleware
```

The module can then be used as `fastapi_proxiedheadersmiddleware` when creating
your FastAPI app:

```python3
from fastapi import FastAPI
from fastapi_proxiedheadersmiddleware import ProxiedHeadersMiddleware

app = FastAPI()
app.add_middleware(ProxiedHeadersMiddleware)
```

The middleware respects the various `X-Forwarded-...` headers and updates the
`Host` header to match.

## Developer quickstart

This project contains a dockerized testing environment which wraps [tox](https://tox.readthedocs.io/en/latest/).

Tests can be run using the `./test.sh` command:

```bash
# Run all PyTest tests and Flake8 checks
$ ./test.sh

# Run just PyTest
$ ./test.sh -e py3

# Run a single test file within PyTest
$ ./test.sh -e py3 -- tests/test_identifiers.py

# Run a single test file within PyTest with verbose logging
$ ./test.sh -e py3 -- tests/test_identifiers.py -vvv
```
