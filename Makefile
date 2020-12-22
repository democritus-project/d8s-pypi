.PHONY: clean clean-test clean-pyc clean-build help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .cache

test: ## run tests quickly with the default Python
	. ~/.virtualenvs/democritus_pypi/bin/activate && py.test
	

coverage: ## check code coverage quickly with the default Python
	. ~/.virtualenvs/democritus_pypi/bin/activate && coverage run --source democritus_pypi -m pytest
	
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	. ~/.virtualenvs/democritus_pypi/bin/activate && pip3 install -r requirements_dev.txt && python setup.py install

upstream: ## set the upstream for the repository
	git remote set-upstream https://gitlab.com/democritus-project/democritus_pypi.git

start: ## start a virtual environment for this project
	virtualenv -p python3 ~/.virtualenvs/democritus_pypi && . ~/.virtualenvs/democritus_pypi/bin/activate && pip3 install -r requirements_dev.txt

destroy: ## destroy the virtual environment for this project
	rm -rf ~/.virtualenvs/democritus_pypi

venv: ## provide info about the virtual environment for this project
	echo '. ~/.virtualenvs/democritus_pypi/bin/activate'
