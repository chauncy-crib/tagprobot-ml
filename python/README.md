# Setup

All our Python code is written using Python 3.7. The following instructions will set up a Python 3.7 virtual environment.

If you don't have `pip3` or `venv` installed (you can check with `pip3 --version`):

```sh
sudo apt install python3-pip
sudo apt install python3.7-venv
```

Make a virtual environment and install dependencies:

```sh
make env
make install
```

# Development

Make sure you are in `tagprobot-ml/python/`.

## Run the code

```sh
make run
```

## Linting + Testing

We use `mypy` for type checking, `flake8` for style enforcement, and `unittest` for tests. You can run them like this:

```sh
make mypy # type checker
make lint # style checker
make test
```

There is also a script which runs all three:

```sh
make build
```

It can also auto-format code first:

```sh
make build_fix
```

## Installing packages

If you add a package, make sure you update `requirements.txt` with:

```sh
make freeze
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

- We bias towards immutability + purity. However, there are performance drawbacks to this approach in Python, so exercise best judgement. A good rule of thumb is that a function should either return a value, or perform a side effect (it should not do both). For side effecting functions, a type annotation of `-> None` indicates the function's purpose is a an effect.
- See [point_update_performance.py](https://github.com/chauncy-crib/tagprobot-ml/blob/master/python/performance/point_update_performance.py) for a performance analysis of different options for handling data.
- We use [dataclasses](https://docs.python.org/3/library/dataclasses.html) heavily to avoid writing class boilerplate. Most classes should be dataclasses. For example:

```
@dataclass(frozen=True)
class MyClass:
    x: int
    y: int
    s: str

my_class = MyClass(x=1, y=2, s="foo")
x = my_class.x
```
