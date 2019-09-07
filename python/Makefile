SHELL = /bin/bash
.PHONY: env install freeze run build
.SILENT: env install freeze run build

activate = source ENV/bin/activate

env:
	python3.7 -m venv ENV

install:
	($(call activate);pip install -r requirements.txt;)

freeze:
	pip freeze > requirements.txt

run:
	($(call activate);./main.py;)

build:
	($(call activate);./build;)
