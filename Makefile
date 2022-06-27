FG_BLACK="\\033[30m"
FG_RED="\\033[31m"
FG_GREEN="\\033[32m"
FG_YELLOW="\\033[33m"
FG_BLUE="\\033[34m"
FG_MAGENTA="\\033[35m"
FG_CYAN="\\033[36m"
FG_WHITE="\\033[37m"
FG_CLEAR="\\033[0m"

modules = clint tests

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: check
check: check-isort check-black check-pylint ## Check current status
	@printf "$(FG_GREEN)Everything is good.$(FG_CLEAN)\n"

.PHONY: check-isort
check-isort: ## Check isort
	@poetry run isort --check --color $(modules)

.PHONY: check-black
check-black: ## Check black
	@poetry run black --check $(modules)

.PHONY: check-pylint
check-pylint: ## Check pylint
	@poetry run pylint --output-format=colorized $(modules)

.PHONY: test
test: ## Run test suite
	@poetry run pytest --cov=clint
