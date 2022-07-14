# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2022-07-14
### Added
- Add change_hook_handler method to runner class.

### Changed
- Better modularization (#39).
- Refactor clint subpackages.
- Change version to 0.4.0.

## [0.3.2] - 2022-07-13
### Changed
- Change status to beta (#37).
- Change project status to beta.
- Update installation information.
- Change version to 0.3.2.
- Rename names of workflows jobs.

## [0.3.1] - 2022-07-12
### Fixed
- Solve validation issues (#35).
- Add validation for comment paragraphs.
- Delete trailing newline in commit messages.
- Solve linters issues.

### Changed
- Add install instructions in one code section.
- Change key features.
- Add hook management examples.
- Change version to 0.3.1.

## [0.3.0] - 2022-07-11
### Added
- Add result management (#32).
- Implement result class.

### Fixed
- Solve error in makefile.
- Solve hook mock fixture issue.

### Changed
- Fix validator tests.
- Fix runner tests.
- Fix hook handler tests.
- Fix command tests.
- Update makefile targets.
- Fix linters issues.
- Change version to 0.3.0.

## [0.2.0] - 2022-07-10
### Added
- Add git hook support (#30).
- Mark message argument as not required.
- Add support to open files.
- Add version option.
- Add git 'commit-msg' hook management options.

### Fixed
- Add correct dir to cli.
- Solve test error on python 3.7.

### Changed
- Add package for testing cli.
- Omit tests dir in coverage report.
- Add package for ci tests.
- Add command class tests for hook invocations.
- Change approach to get root directory.
- Add hook handler class tests.
- Delete unused variable.
- Change version to 0.2.0.

## [0.1.3] - 2022-07-06
### Changed
- Add installation instructions (#26).
- Add installation instructions.
- Change version to 0.1.3.

## [0.1.2] - 2022-07-06
### Fixed
- Validation version events (#25).
- Change version validation to run only on PRs.

### Changed
- Split test-and-lint action.
- Change version to 0.1.2.

## [0.1.1] - 2022-07-06
### Fixed
- Add setup-python id to respective step.
- Rename version validation action title.
- Change python version to string.

### Changed
- Validate version changes (#22).
- Validate package version against metadata.
- Add ci version validation test.
- Add version validation github action.
- Add more pypi classifiers.
- Change project name for clint-cli.
- Change version to 0.1.1.
- Add publish github action.

## [0.1.0] - 2022-07-05
### Added
- Add repl target to makefile (#11).
- Enhance makefile check targets output (#5).
- Validate numpy docstrings (#4).
- First validator implementation (#3).
- Add validation workflow (#1).

### Changed
- Improve readme (#21).
- Add codeowners file (#19).
- Object oriented approach (#10).
- Change validation tools (#2).
- Add makefile for ease of use.
- Add coverage tool.
- Add readme title.
- Config dependencies.
- Initial commit.

[Unreleased]: https://github.com/rcisterna/clint/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/rcisterna/clint/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/rcisterna/clint/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/rcisterna/clint/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/rcisterna/clint/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/rcisterna/clint/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/rcisterna/clint/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/rcisterna/clint/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/rcisterna/clint/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/rcisterna/clint/releases/tag/v0.1.0
