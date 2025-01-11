build: test .venv/bin/zderad

deploy: build
	pipx install .

test: zderad/**/* tests/**/*
	.venv/bin/flake8 --exit-zero zderad --exclude \*\*/__init__.py
	.venv/bin/pytest

.venv/bin/zderad: zderad/**/* setup.py
	.venv/bin/pip3 install .
