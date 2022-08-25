setup-project:

	echo INIT GIT
	git init
	echo 
	echo CREATE VENV
	python -m venv venv
	echo UPDATE PIP
	venv/bin/python -m pip install --upgrade pip
	echo 
	echo INSTALLING PACKAGE
	venv/bin/pip install -e .
	echo 
	echo INSTALLING DEV DEPENDENCIES
	venv/bin/pip install -r requirements_dev.txt
	echo 
	echo CREATE HOOK
	echo "#!/bin/sh" > .git/hooks/pre-commit 
	echo "pytest -sv" >> .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	python -m pytest

install:
	python -m pip install --upgrade .
    
install-dev: requirements_dev.txt
	pip install -r requirements_dev.txt

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rdf htmlcov
	rm .coverage
	rm -rdf build

lint: 
	isort {{cookiecutter.package_name}} tests
	black {{cookiecutter.package_name}} tests 
	vulture {{cookiecutter.package_name}} --min-confidence 90
	flake8 {{cookiecutter.package_name}} 
		
cov:
	pytest --cov-report term:skip-covered --cov-report html --cov={{cookiecutter.package_name}} tests

