export PATH := .venv/bin:$(PATH)

build: test
	pip3 install -e .

install: build
	pipx install . --force

test: zderad/**/* tests/**/*
	flake8 --exit-zero zderad --exclude \*\*/__init__.py
	pytest

run: build
	zderad -D --output-file debug/output.docx

.PHONY: test
