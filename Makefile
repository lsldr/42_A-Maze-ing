all: run

install:
	@uv sync

run:
	@uv run main.py

debug:
	@uv run -m pdb main.py

clean:
	@rm -Rf .mypy_cache
	@find . -depth -name __pycache__ -type d -not -path "./.venv/*" -exec rm -r {} +

lint:
	@flake8 . --extend-exclude .venv
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports\
			--disallow-untyped-defs --check-untyped-defs --exclude ./.venv/
lint-strict:
	@flake8 . --extend-exclude .venv
	@mypy . --strict --exclude ./.venv/

.PHONY: install run debug clean lint lint-strict 
