"""Tests suite for CLI classes."""
import pytest
from click.testing import CliRunner

from clint import validator


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture to get a CliRunner instance."""
    return CliRunner()


@pytest.fixture(scope="class")
def mock_command_show_result(request, class_mocker):
    """Fixture to patch cli.command.Command.show_result method."""
    request.cls.mock_command_show_result = class_mocker.patch(
        "clint.cli.command.Command.show_result"
    )


@pytest.fixture(scope="class")
def mock_runner_validate(request, class_mocker):
    """Fixture to patch cli.runner.Runner.validate method."""
    request.cls.mock_runner_validate = class_mocker.patch(
        "clint.cli.runner.Runner.validate"
    )


@pytest.fixture(scope="class")
def mock_commit_generate(request, class_mocker):
    """Fixture to patch clint.validator.Commit.generate method."""
    request.cls.mock_commit_generate = class_mocker.patch(
        "clint.validator.Commit.generate", return_value=validator.Commit("")
    )


@pytest.fixture(scope="class")
def mock_commit_validate(request, class_mocker):
    """Fixture to patch clint.validator.Commit.validate method."""
    request.cls.mock_commit_validate = class_mocker.patch(
        "clint.validator.Commit.validate", return_value=True
    )


@pytest.fixture(scope="class")
def mock_click_echo(request, class_mocker):
    """Fixture to patch clint.validator.Commit.validate method."""
    request.cls.mock_click_echo = class_mocker.patch("click.echo")


@pytest.fixture
def clean_commit_mocks(request: pytest.FixtureRequest):
    """Fixture to reset mock_subject_validate and mock_paragraph_validate."""
    request.cls.mock_commit_generate.reset_mock()
    request.cls.mock_commit_generate.side_effect = None
    request.cls.mock_commit_validate.reset_mock()
    request.cls.mock_commit_validate.side_effect = None
