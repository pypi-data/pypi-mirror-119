# Hello G

This is for testing upload package to PyPI.

## Installation
Run the following to install:
```python
pip install helloG
```

## Usage
```python
from helloG import say_hello

# Generate "Hello World"
say_hello()

# Generate "Hello, <name>"
say_hello("<name>")
```

## Developing HelloG
To install helloG, along with the tools you need to develop and run tests, run the following in your virtualenv:
```bash
$ pip install -e .[dev]
```