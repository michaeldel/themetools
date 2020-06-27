run:
	python -m themetools

lint:
	black --check .
	flake8

test:
	pytest

data:
	./scripts/download.sh

clean:
	@rm -r data

.PHONY: run lint test clean

