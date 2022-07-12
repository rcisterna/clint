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

.PHONY: repl
repl: ## Open new REPL
	@poetry run bpython

.PHONY: check
check: check-isort check-docs check-black check-pylint ## Check current status
	@true

.PHONY: check-isort
check-isort:
	@printf "$(FG_BLUE)Running isort:$(FG_CLEAR)\n"
	@poetry run isort --check --color $(modules) \
	&& printf "$(FG_GREEN)isort found no issues.$(FG_CLEAR)\n\n" \
	|| (printf "$(FG_RED)Issues below were found by isort.$(FG_CLEAR)\n\n" && false)

.PHONY: check-docs
check-docs:
	@printf "$(FG_BLUE)Running pydocstyle:$(FG_CLEAR)\n"
	@poetry run pydocstyle $(modules) \
	&& printf "$(FG_GREEN)pydocstyle found no issues.$(FG_CLEAR)\n\n" \
	|| (printf "$(FG_RED)Issues below were found by pydocstyle.$(FG_CLEAR)\n\n" && false)

.PHONY: check-black
check-black:
	@printf "$(FG_BLUE)Running black:$(FG_CLEAR)\n"
	@poetry run black --check $(modules) \
	&& printf "$(FG_GREEN)black found no issues.$(FG_CLEAR)\n\n" \
	|| (printf "$(FG_RED)Issues below were found by black.$(FG_CLEAR)\n\n" && false)

.PHONY: check-pylint
check-pylint:
	@printf "$(FG_BLUE)Running pylint:$(FG_CLEAR)\n"
	@poetry run pylint --output-format=colorized --score=n $(modules) \
	&& printf "$(FG_GREEN)pylint found no issues.$(FG_CLEAR)\n\n" \
	|| (printf "$(FG_RED)Issues below were found by pylint.$(FG_CLEAR)\n\n" && false)

.PHONY: tests
tests: ## Run test suite, except the CI tests
	@poetry run coverage erase
	@poetry run coverage run -m pytest -m "not ci_version" --strict-markers
	@printf "\n$(FG_BLUE)Coverage report:$(FG_CLEAR)\n\n"
	@poetry run coverage report -m

.PHONY: tests-ci-version
tests-ci-version: ## Run the CI version tests
	@poetry run pytest -m ci_version

.PHONY: isort
isort:  ## Run isort over staged files
	@poetry run isort clint tests

.PHONY: black
black:  ## Run black over staged files
	@poetry run black clint tests

.PHONY: pylint
pylint:  ## Run pylint over staged files
	@poetry run pylint clint tests --output-format=colorized
