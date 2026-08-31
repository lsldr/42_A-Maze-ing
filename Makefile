all: run

install:
	@uv sync

run:
	@uv run a_maze_ing.py config.txt

debug:
	@uv run -m pdb a_maze_ing.py config.txt

pytest-fast:
	@uv run --with pytest --with pytest-cov python -m pytest mazegen/tests -q -ra --maxfail=1

pytest-verbose:
	@uv run --with pytest --with pytest-cov python -m pytest mazegen/tests -vv -ra --maxfail=1

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

.PHONY: install run debug clean lint lint-strict pytest-fast pytest-verbose
