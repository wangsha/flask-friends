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
	pipenv install --dev

lint:
	pipenv run black --check .
	flake8

test .coverage: lint
	pipenv run python -m pytest -l tests

cov: .coverage
	@coverage report --skip-covered

htmlcov: .coverage
	@coverage html --skip-covered
	@echo "open htmlcov/index.html"

htmlcov-debug: clean
	$(MAKE) htmlcov -i
