# Setup

If you don't have `pip3` installed (you can check with `pip3 --version`):

```
sudo apt install python3-pip
```

Install `virtualenv`:

```
sudo apt install python3-venv
```

Make a virtual environment. We are using 3.7:

```
python3.7 -m venv ENV
```

Activate the virtual environment:

```
source ENV/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

# Development

## Installing packages

If you add a package, make sure you update `requirements.txt` with:

```
pip freeze > requirements.txt
```

## Type checking

```
mypy . # can put any folder or .py file here
```
