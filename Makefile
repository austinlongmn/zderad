export PATH := .venv/bin:$(PATH)

build: test

install: build
	pipx install . --force

test: zderad/**/* tests/**/*
	flake8 --exit-zero zderad --exclude \*\*/__init__.py
	pytest

run: build
	zderad -D --output-file debug/output.docx

setup:
	pip3 install setuptools pytest flake8
	pip3 install -e .

.PHONY: test
