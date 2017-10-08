.PHONY: clean clean-test clean-pyc
clean: clean-test clean-pyc


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage*
	rm -fr htmlcov
	rm -f junit.xml

install: clean
	pip install -r requirements.txt
	pip install -e .

lint:
	flake8

test .coverage:
	pytest --cov-report=term:skip-covered --cov=friends --cov-branch

cov: .coverage
	@coverage report --skip-covered

htmlcov: .coverage
	@coverage html --skip-covered
	@echo "open htmlcov/index.html"

htmlcov-debug: clean
	$(MAKE) htmlcov -i
