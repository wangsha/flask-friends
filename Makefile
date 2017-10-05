.PHONY: clean clean-test clean-pyc
clean: clean-test clean-pyc
ENV:=dev


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
	pip install -r requirements/${ENV}.txt

lint:
	flake8

lint-changes:
	flake8 $$(git status -s | grep -E '\.py$$' | cut -c 4-)

test .coverage:
	pytest --cov-report= --cov=pd --cov-fail-under=100 --reset-db --schema-mode=alembic pd

cov: .coverage
	@coverage report --skip-covered

htmlcov: .coverage
	@coverage html --skip-covered
	@echo "open htmlcov/index.html"

htmlcov-debug: clean
	$(MAKE) htmlcov -i
