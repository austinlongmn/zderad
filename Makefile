build: test .venv/bin/zderad

deploy: build
	pipx install .

test: zderad/**/*
	.venv/bin/pytest

.venv/bin/zderad: zderad/**/* setup.py
	.venv/bin/pip3 install .
