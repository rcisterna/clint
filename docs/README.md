# CLint: Conventional commits linter

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![es](https://img.shields.io/badge/lang-es-green.svg)](README.es.md)

`CLint` is a command line tool that allows you to validate messages related to git commits in different ways, ensuring
that the message is [Conventional Commits compliant](https://www.conventionalcommits.org/en/v1.0.0/#specification).

## Technologies

- [Python](https://www.python.org/) 3.7.2+
- [Poetry](https://python-poetry.org/)

## Key features

- Validate a commit message in the command line.

## Planned features

- Allow to handle git `commit-msg` hook.
- Make [pre-commit](https://pre-commit.com/) compatible.
- Validate a commit message in the command line through pipes.
- Allow to build a commit message through command line prompts.

## Usage examples

```sh
# Validate a sample message
$ clint "feat(scope): validate this message"
Your commit message is CC compliant!
```

```sh
# Validation error for invalid type (typo)
$ clint "feta(scope): validate this message"
Validation error: Type 'feta' is not valid.
```

## Project status

`CLint` is currently under active development. The goal is to achieve at least the [planned features](#planned-features)
, and then continue maintaining the code, making it compatible with future versions of Python and the libraries used in
the project.

## Source

`CLint` tries to be what other tools already are, like the
great [commitlint](https://github.com/conventional-changelog/commitlint). The difference
with [similar tools](https://www.conventionalcommits.org/en/about/#tooling-for-conventional-commits) is that those are
built over `Node.js`, so they are focused on `Javascript` developers. If you are not, you will be forced to
install `Node.js` anyway in order to use those tools.
