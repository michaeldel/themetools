run:
	python -m themetools

lint:
	black --check .
	flake8

test:
	pytest

.PHONY: run lint test

