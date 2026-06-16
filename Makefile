# One-command targets for the benchmark.
#
# Windows note: `make` is not installed by default. Either run the underlying
# `uv run ...` command shown in each target directly, or use WSL / Git Bash with
# `make` installed. The commands themselves are cross-platform.

.PHONY: install run score chart test clean

install:        ## create the venv and install dependencies
	uv sync

run:            ## call every model x ticket x repeat -> results/raw_calls.csv
	uv run python -m src.runner

score:          ## aggregate raw calls -> results/summary.csv
	uv run python -m src.aggregate

chart:          ## render results/pareto.png from the summary
	uv run python -m src.chart

test:           ## run the scorer/parser unit tests
	uv run pytest -q

clean:          ## remove generated results (keeps the golden set)
	rm -f results/raw_calls.csv results/summary.csv results/pareto.png
