[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Installation

```pip install futurelog```

# Usage

## Introduction

The goal of this library is to provide a way to defer logs and consume (print) them when needed, in an async application.

For instance, it would perfectly fit a config deployer in async. It would help to keep messages grouped by servers.

Usage should be limited to reporting and not error/exception logging.
Also you should ensure you catch all possible exception in your program in your entrypoint, in order to consume all logs before exiting your application.

## Create a logger

```python
from futurelog import FutureLogger

future_logger = FutureLogger(__name__)
```

## Register logs

The methods supported are: `.debug()`, `.info()`, `.warning()`, `.error()`, `.critical()`

```python
future_logger.debug(topic, msg)
```

Example:
```python
future_logger.debug("server1", "deploying stuff 1")
future_logger.error("server1", "failed")
future_logger.debug("server2", "deploying stuff 1")
future_logger.warning("server2", "success")
```

## Consume logs

### One specific logger

```python
logger.consume(topic)
```

Example:
```python
future_logger.consume("server1")
future_logger.consume("server2")
```

### All loggers for a topic (one for each module)

```python
FutureLogger.consume_all_logger_for(topic)
```

```python
FutureLogger.consume_all_logger_for("server1")
FutureLogger.consume_all_logger_for("server2")
```

### All unconsumed logger

```python
FutureLogger.consume_all_logger()
```
