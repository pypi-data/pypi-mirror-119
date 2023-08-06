# Belvaio Request Id

[![Package version](https://img.shields.io/pypi/v/belvaio-request-id)](https://pypi.org/project/belvaio-request-id/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/belvaio-request-id)](https://pypistats.org/packages/belvaio-request-id)
[![Build Status](https://travis-ci.com/belvo-finance/belvaio-request-id.svg?branch=master)](https://travis-ci.com/belvo-finance/belvaio-request-id)
[![codecov](https://codecov.io/gh/belvo-finance/belvaio-request-id/branch/master/graph/badge.svg)](https://codecov.io/gh/belvo-finance/belvaio-request-id)

Belvaio Request Id is an [aiohttp][aiohttp] set of utils that help us to track request journey between services.

1. **`request_id_middleware`**: aiohttp middleware that generate random `request_id` or read it from `X-Request-Id` header for each http request.

2. **`RequestIdFilter`**: logging filter that allow attach `request_id` to every logging record.

3. **`RequestIdAccessLogger`**: add `request_id` to aiohttp access log. This log message is logged outside the scope where we set the context var that store the `request_id`, so we need to define our own [AccessLogger][access-logs] that fixes this.

4. If [Sentry][sentry-aiohttp] is used  a `request_id` tag is added when the http request is processed.

Motivation: [Skyscanner / aiotask-context][motivation]

## Requirements

- Python 3.7+
- [`aiohttp`][aiohttp] >= 3.5

## Installation

```shell
pip install belvaio-request-id
```

## Example

```python
"""
POC to demonstrate the usage of the belvaio-request-id package for writing the request_id from aiohttp into every log call. If you run this script, you can try to query with curl or the browser:

    $ curl http://127.0.0.1:8080/Mateu
    Hello, Mateu. Your request id is 93234aa6d4524f4bb76622e5d0c85589.

    $ curl -H "X-Request-ID: e72ec21b412845cf86a8aee50331cc4f" http://127.0.0.1:8080/Mateu
    Hello, Mateu. Your request id is e72ec21b412845cf86a8aee50331cc4f.

In the terminal you should see something similar to:

    ======== Running on http://0.0.0.0:8080 ========
    (Press CTRL+C to quit)
    2020-03-20 11:43:20,248 INFO __main__ 93234aa6d4524f4bb76622e5d0c85589 | Received new GET /Mateu call
    2020-03-20 11:43:20,249 INFO aiohttp.access 93234aa6d4524f4bb76622e5d0c85589 | 127.0.0.1 "GET /Mateu HTTP/1.1" 200 266 "curl/7.64.1"
"""

import logging.config

from aiohttp import web
from belvaio_request_id.logger import RequestIdAccessLogger
from belvaio_request_id.middleware import request_id_middleware
from belvaio_request_id.utils import get_request_id

LOG_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "filters": ["requestid"],
        },
    },
    "filters": {"requestid": {"()": "belvaio_request_id.logger.RequestIdFilter",},},
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s %(request_id)s | %(message)s",
        },
    },
    "loggers": {"": {"level": "DEBUG", "handlers": ["console"], "propagate": True},},
}

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger(__name__)


async def handle(request):
    name = request.match_info.get("name")
    logger.info("Received new GET /%s call", name)
    text = f"Hello, {name}. Your request id is {get_request_id()}.\n"
    return web.Response(text=text)


if __name__ == "__main__":
    app = web.Application(middlewares=[request_id_middleware])
    app.router.add_route("GET", "/{name}", handle)
    web.run_app(
        app,
        access_log_format='%a "%r" %s %b "%{User-Agent}i"',
        access_log_class=RequestIdAccessLogger,
    )

```

## Contributing

The Belvo team happily welcomes contributions.
If you wish to submit a pull request, please be sure check the items on this list:
- [ ] Tests related to the changed code were executed
- [ ] The source code has been coded following the OWASP security best practices (https://owasp.org/www-pdf-archive/OWASP_SCP_Quick_Reference_Guide_v2.pdf).
- [ ] Commit message properly labeled
- [ ] There is a ticket associated to each PR.

[Guidelines][guidelines] will help you get ready to contribute to this project!

[aiohttp]: https://docs.aiohttp.org/en/stable/index.html
[guidelines]: https://github.com/belvo-finance/belvaio-request-id/blob/master/CONTRIBUTING.md
[access-logs]: https://docs.aiohttp.org/en/stable/logging.html#access-logs
[sentry-aiohttp]: https://docs.sentry.io/platforms/python/aiohttp/
[motivation]: https://github.com/Skyscanner/aiotask-context

 
