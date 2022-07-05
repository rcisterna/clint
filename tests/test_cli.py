"""Test suite for CLI class."""
from unittest.mock import MagicMock, call

import pytest

from clint import validator
from clint.cli import CLI


@pytest.mark.usefixtures("mock_validate_commit_message")
class TestCLIEntrypoint:
    """Tests for clint.cli.CLI.entrypoint method."""

    mock_validate_commit_message: MagicMock

    def test_valid_invocation(self, cli_runner, sentence):
        """Test valid invocation of the entrypoint."""
        self.mock_validate_commit_message.reset_mock()
        msg = f"feat: {sentence}"
        result = cli_runner.invoke(CLI.entrypoint, [msg])
        assert self.mock_validate_commit_message.call_args_list == [call(message=msg)]
        assert not result.exception
        assert result.exit_code == 0

    def test_empty_invocation(self, cli_runner):
        """Test invocation of the entrypoint with no arguments."""
        self.mock_validate_commit_message.reset_mock()
        result = cli_runner.invoke(CLI.entrypoint)
        assert not self.mock_validate_commit_message.called
        assert result.exception
        assert result.exit_code == 2


@pytest.mark.usefixtures(
    "mock_commit_generate", "mock_commit_validate", "mock_click_echo"
)
class TestCLIValidateCommitMessage:
    """Tests for clint.cli.CLI.validate_commit_message method."""

    # pylint: disable=unused-argument

    mock_commit_generate: MagicMock
    mock_commit_validate: MagicMock
    mock_click_echo: MagicMock

    def test_valid_execution(self, clean_commit_mocks):
        """Test valid execution of validate_commit_message method."""
        message = "message"
        CLI.validate_commit_message(message=message)
        assert self.mock_commit_generate.call_args_list == [call(msg=message)]
        assert self.mock_commit_validate.call_args_list == [call()]
        self.mock_click_echo.call_args_list = [
            call("Your commit message is CC compliant!")
        ]

    def test_generation_exception(self, clean_commit_mocks):
        """Test exception handling on validate_commit_message method."""
        error = "error"
        message = "message"
        self.mock_commit_generate.side_effect = validator.GenerationException(error)
        CLI.validate_commit_message(message=message)
        assert self.mock_commit_generate.call_args_list == [call(msg=message)]
        assert not self.mock_commit_validate.called
        assert self.mock_click_echo.call_args_list == [call(f"Parsing error: {error}")]

    def test_validation_exception(self, clean_commit_mocks):
        """Test exception handling on validate_commit_message method."""
        error = "error"
        message = "message"
        self.mock_commit_validate.side_effect = validator.ValidationException(error)
        CLI.validate_commit_message(message=message)
        assert self.mock_commit_generate.call_args_list == [call(msg=message)]
        assert self.mock_commit_validate.call_args_list == [call()]
        self.mock_click_echo.call_args_list = [call(f"Validation error: {error}")]
