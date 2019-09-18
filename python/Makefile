SHELL = /bin/bash
.PHONY: env install freeze run mypy lint test build build_fix

activate = source ENV/bin/activate

env:
	python3.7 -m venv ENV

install:
	($(call activate);pip install -r requirements.txt;)

freeze:
	($(call activate);pip freeze > requirements.txt;)

run:
	($(call activate);python main.py;)

mypy:
	($(call activate);mypy .;)

lint:
	($(call activate);flake8;)

test:
	($(call activate);python -m unittest;)

build:
	($(call activate);./build;)

build_fix:
	($(call activate);./build --fix;)
