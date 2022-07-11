"""Test suite for CLI class."""
from unittest.mock import MagicMock, call

import pytest

from clint import validator
from clint.cli.runner import Runner


@pytest.mark.usefixtures("mock_commit_generate", "mock_commit_validate")
class TestRunnerValidate:
    """Tests for clint.cli.runner.Runner.validate method."""

    # pylint: disable=unused-argument

    mock_commit_generate: MagicMock
    mock_commit_validate: MagicMock

    def test_valid_execution(self, clean_commit_mocks):
        """Test valid execution of validate method."""
        message = "message"
        Runner.validate(message=message)
        assert self.mock_commit_generate.call_args_list == [call(msg=message)]
        assert self.mock_commit_validate.call_args_list == [call()]

    def test_generation_exception(self, clean_commit_mocks):
        """Test exception handling on validate method."""
        error = "error"
        message = "message"
        self.mock_commit_generate.side_effect = validator.GenerationException(error)
        result = Runner.validate(message=message)
        assert result.actions == {"generation": error}
        assert result.return_code == 101
        assert self.mock_commit_generate.call_args_list == [call(msg=message)]
        assert not self.mock_commit_validate.called

    def test_validation_exception(self, clean_commit_mocks):
        """Test exception handling on validate method."""
        error = "error"
        message = "message"
        self.mock_commit_validate.side_effect = validator.ValidationException(error)
        result = Runner.validate(message=message)
        assert result.actions == {"validation": error}
        assert result.return_code == 101
        assert self.mock_commit_generate.call_args_list == [call(msg=message)]
        assert self.mock_commit_validate.call_args_list == [call()]
