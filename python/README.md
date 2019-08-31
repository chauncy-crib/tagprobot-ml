# Setup

All our Python code is written using Python 3.7. The following instructions will set up a Python 3.7 virtual environment.

If you don't have `pip3` or `venv` installed (you can check with `pip3 --version`):

```
sudo apt install python3-pip
sudo apt install python3.7-venv
```

Make a virtual environment and install dependencies:

```
python3.7 -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
```

# Development

Make sure you are in `tagprobot-ml/python/`, and have `ENV` activated.

## Run the code

`python main.py`

## Linting + Testing

```
mypy . # type checker
flake8 # style checker
python -m unittest
```

## Installing packages

If you add a package, make sure you update `requirements.txt` with:

```
pip freeze > requirements.txt
```

# Style guide

## Types

- Use [type hints](https://docs.python.org/3/library/typing.html) for function and class arguments. For self-referential classes, use string literals to denote types. This is a work-around of a Python peculariarity, where you cannot reference a class until _after_ it has been defined. For example, to write a linked-list node class, we annotate it like this:

```
class Node:
    """Binary tree node."""

    def __init__(self, left: 'Node', right: 'Node'):
        self.left = left
        self.right = right
```


- Use [reST-style](http://queirozf.com/entries/python-docstrings-reference-examples#restructuredtext-rest-docstring-example) docstrings for functions when the type annotations are not sufficient documentation.

## Immutability + Purity

- We bias towards immutability + purity. For example, we tend to use [frozen dataclasses](https://docs.python.org/3/library/dataclasses.html) to represent immutable collections of data.

```
@dataclass(frozen=True)
class MyClass:
    x: int
    y: int
    s: str
    pass
```
