build: .venv/bin/zderad

deploy: build
	pipx install .

.venv/bin/zderad: zderad/**/* setup.py
	.venv/bin/pip3 install .
