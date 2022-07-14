"""Test suite for CLI class."""
from unittest.mock import MagicMock, call

import pytest

from clint import validator
from clint.cli.runner import Runner
from clint.hook_handler import HookException, HookHandler

from .conftest import get_result


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


@pytest.mark.usefixtures("hook_handler_methods")
class TestRunnerChangeHookHandler:
    """Tests for clint.cli.runner.Runner.change_hook_handler method."""

    # pylint: disable=unused-argument

    mock_hook_get_repo_root: MagicMock
    mock_hook_enable: MagicMock
    mock_hook_disable: MagicMock

    results = []

    @pytest.mark.parametrize("is_enabling", [True, False])
    def test_hook_outside_repo(self, sentence, clean_hook_handler_methods, is_enabling):
        """Test invocation of the entrypoint for git hook outside repo directory."""
        self.mock_hook_get_repo_root.side_effect = HookException(sentence)
        result = Runner.change_hook_handler(is_enabling=is_enabling)
        assert result.actions == {
            f"{'Enable' if is_enabling else 'Disable'} hook": sentence
        }
        assert result.return_code == HookHandler.OPERATION_BASE_ERROR_CODE + 1
        assert self.mock_hook_get_repo_root.call_args_list == [call()]
        assert not self.mock_hook_enable.called
        assert not self.mock_hook_disable.called

    def test_hook_enable(self, clean_hook_handler_methods, sentence):
        """Test invocation of the entrypoint to enable git hook."""
        result = get_result().add_action(
            action="action", message=sentence, is_error=False
        )
        self.mock_hook_enable.return_value = result
        hook_result = Runner.change_hook_handler(is_enabling=True)
        assert hook_result == result
        assert self.mock_hook_get_repo_root.call_args_list == [call()]
        assert self.mock_hook_enable.call_args_list == [call()]
        assert not self.mock_hook_disable.called

    def test_hook_disable(self, cli_runner, clean_hook_handler_methods, sentence):
        """Test invocation of the entrypoint to disable git hook."""
        result = get_result().add_action(
            action="action", message=sentence, is_error=False
        )
        self.mock_hook_disable.return_value = result
        hook_result = Runner.change_hook_handler(is_enabling=False)
        assert hook_result == result
        assert self.mock_hook_get_repo_root.call_args_list == [call()]
        assert not self.mock_hook_enable.called
        assert self.mock_hook_disable.call_args_list == [call()]
