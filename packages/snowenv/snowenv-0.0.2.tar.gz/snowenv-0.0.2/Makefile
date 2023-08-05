build: clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build dist

requirements:
	pip3 install -r requirements.txt 
	pip3 install -r requirements-test.txt
.PHONY: requirements

fmt:
	black .

check-fmt:
	black --check .
.PHONY: check-fmt

check-lint:
	pylint snowenv
.PHONY: check-lint

check-type:
	mypy snowenv
.PHONY: check-type

check: check-fmt check-lint check-type
.PHONY: check

test:
	python3 -m unittest tests
.PHONY: test

dev-install: build
	pip3 uninstall -y snowenv && pip3 install dist/snowenv-*-py3-none-any.whl
.PHONY: dev-install
