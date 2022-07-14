# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2022-07-14
### Fixed
- Change metadata_production fixture to class scope.

### Changed
- Add changelog file.
- Add changelog tests marked for ci.
- Update test targets for makefile.
- Add workflow for changelog validation.

## [0.4.0] - 2022-07-14
### Added
- Add change_hook_handler method to runner class.

### Changed
- Refactor clint subpackages.

## [0.3.2] - 2022-07-13
### Changed
- Change project status to beta.
- Update installation information.
- Rename names of workflows jobs.

## [0.3.1] - 2022-07-12
### Fixed
- Add validation for comment paragraphs.
- Delete trailing newline in commit messages.
- Solve linters issues.

### Changed
- Add install instructions in one code section.
- Change key features.
- Add hook management examples.

## [0.3.0] - 2022-07-11
### Added
- Add result management class.

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

## [0.2.0] - 2022-07-10
### Added
- Add git hook support.
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

## [0.1.3] - 2022-07-06
### Changed
- Add installation instructions.

## [0.1.2] - 2022-07-06
### Fixed
- Change version validation to run only on PRs.

### Changed
- Split test-and-lint action.

## [0.1.1] - 2022-07-06
### Fixed
- Add setup-python id to respective step.
- Rename version validation action title.
- Change python version to string.

### Changed
- Validate package version against metadata.
- Add ci version validation test.
- Add version validation github action.
- Add more pypi classifiers.
- Change project name for clint-cli.
- Add publish github action.

## [0.1.0] - 2022-07-05
### Added
- Add repl target to makefile.
- Enhance makefile check targets output.
- Validate numpy docstrings.
- First validator implementation.
- Add validation workflow.

### Changed
- Improve readme.
- Add codeowners file.
- Object-oriented approach.
- Add makefile for ease of use.
- Add coverage tool.
- Add readme title.
- Config dependencies.

[Unreleased]: https://github.com/rcisterna/clint/compare/v0.4.1...HEAD
[0.4.1]: https://github.com/rcisterna/clint/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/rcisterna/clint/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/rcisterna/clint/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/rcisterna/clint/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/rcisterna/clint/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/rcisterna/clint/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/rcisterna/clint/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/rcisterna/clint/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/rcisterna/clint/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/rcisterna/clint/releases/tag/v0.1.0
