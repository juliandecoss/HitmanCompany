SHELL=/bin/bash
PATH := .venv/bin:$(PATH)

start:
	@( \
		source .venv/bin/activate; \
		flask run \
	)
install:
	@[ ! -d .venv ] && python3 -m venv --copies .venv ||:;
	@( \
		source .venv/bin/activate; \
		pip install -qU pip; \
		pip install -r requirements.txt; \
	)

mypy:
	@mypy src;

lint: mypy black isort autoflake

lint-fix: #mypy
	@black --exclude '.venv|build|target|dist|.cache|node_modules' .;
	@isort -q -l=250 --force-single-line-imports .;
	@autoflake --in-place --recursive --exclude '.venv,build,target,dist,.cache,node_modules' --remove-all-unused-imports --remove-unused-variables .;
	@isort -q .;