.PHONY: pylint test black precommit ci

pylint:
	python3 -m pylint --version
	python3 -m pylint shapes user_app widget_project

test:
	python3 -m pytest --version
	python3 -m pytest "shapes/tests/unit"

black:
	python3 -m black --version
	python3 -m black shapes

precommit:
	@echo "Setting up pre-commit..."
	./.venv/bin/pre-commit install
	./.venv/bin/pre-commit autoupdate

ci: precommit pylint black test
