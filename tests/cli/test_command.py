"""Test suite for CLI class."""
from unittest.mock import MagicMock, call

import pytest

from clint.cli.command import Command
from clint.hook_handler import HookException, HookHandler
from clint.result import Result


@pytest.mark.usefixtures(
    "mock_runner_validate", "mock_command_show_result", "hook_handler_methods"
)
class TestCommandEntrypoint:
    """Tests for clint.cli.command.Command.entrypoint method."""

    # pylint: disable=unused-argument

    mock_runner_validate: MagicMock
    mock_command_show_result: MagicMock
    mock_hook_get_repo_root: MagicMock
    mock_hook_enable: MagicMock
    mock_hook_disable: MagicMock

    results = [
        Result(operation="test", base_error_code=0),
        Result(operation="test", base_error_code=0).add_action(
            action="no_error", message="message", is_error=False
        ),
        Result(operation="test", base_error_code=0).add_action(
            action="error", message="message", is_error=True
        ),
        Result(operation="test", base_error_code=0)
        .add_action(action="error", message="message", is_error=True)
        .add_action(action="no_error", message="message", is_error=False),
        Result(operation="test", base_error_code=0)
        .add_action(action="no_error", message="message", is_error=False)
        .add_action(action="error", message="message", is_error=True),
    ]

    @pytest.mark.parametrize("result", results)
    def test_with_message(self, cli_runner, sentence, result):
        """Test invocation of the entrypoint with message."""
        self.mock_runner_validate.reset_mock()
        self.mock_runner_validate.return_value = result
        self.mock_command_show_result.reset_mock()
        cmd_result = cli_runner.invoke(Command.entrypoint, [sentence])
        assert self.mock_runner_validate.call_args_list == [call(message=sentence)]
        assert self.mock_command_show_result.call_args_list == [call(result=result)]
        assert cmd_result.exit_code == result.return_code

    @pytest.mark.parametrize("result", results)
    def test_with_file(self, cli_runner, sentence, result):
        """Test invocation of the entrypoint with file."""
        self.mock_runner_validate.reset_mock()
        self.mock_runner_validate.return_value = result
        self.mock_command_show_result.reset_mock()
        with cli_runner.isolated_filesystem():
            filename = "example.txt"
            with open(filename, "w", encoding="utf8") as temp_file:
                temp_file.write(sentence)
            cmd_result = cli_runner.invoke(Command.entrypoint, ["--file", filename])
        assert self.mock_runner_validate.call_args_list == [call(message=sentence)]
        assert self.mock_command_show_result.call_args_list == [call(result=result)]
        assert cmd_result.exit_code == result.return_code

    def test_empty_invocation(self, cli_runner):
        """Test invocation of the entrypoint with no arguments."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        cmd_result = cli_runner.invoke(Command.entrypoint)
        assert not self.mock_runner_validate.called
        assert not self.mock_command_show_result.called
        assert cmd_result.exit_code == 0

    @pytest.mark.parametrize("hook_flag", ["--enable-hook", "--disable-hook"])
    def test_hook_outside_repo(
        self, hook_flag, cli_runner, sentence, clean_hook_handler_methods
    ):
        """Test invocation of the entrypoint for git hook outside repo directory."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        self.mock_hook_get_repo_root.side_effect = HookException(sentence)
        cmd_result = cli_runner.invoke(Command.entrypoint, [hook_flag])
        assert self.mock_hook_get_repo_root.call_args_list == [call()]
        assert not self.mock_hook_enable.called
        assert not self.mock_hook_disable.called
        assert not self.mock_runner_validate.called
        assert self.mock_command_show_result.called
        assert cmd_result.exit_code == HookHandler.OPERATION_BASE_ERROR_CODE + 1

    @pytest.mark.parametrize("result", results)
    def test_hook_enable(self, cli_runner, clean_hook_handler_methods, result):
        """Test invocation of the entrypoint to enable git hook."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        self.mock_hook_enable.return_value = result
        cmd_result = cli_runner.invoke(Command.entrypoint, ["--enable-hook"])
        assert self.mock_hook_get_repo_root.call_args_list == [call()]
        assert self.mock_hook_enable.call_args_list == [call()]
        assert not self.mock_hook_disable.called
        assert not self.mock_runner_validate.called
        assert self.mock_command_show_result.call_args_list == [call(result=result)]
        assert cmd_result.exit_code == result.return_code

    @pytest.mark.parametrize("result", results)
    def test_hook_disable(self, cli_runner, clean_hook_handler_methods, result):
        """Test invocation of the entrypoint to disable git hook."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        self.mock_hook_disable.return_value = result
        cmd_result = cli_runner.invoke(Command.entrypoint, ["--disable-hook"])
        assert self.mock_hook_get_repo_root.call_args_list == [call()]
        assert not self.mock_hook_enable.called
        assert self.mock_hook_disable.call_args_list == [call()]
        assert not self.mock_runner_validate.called
        assert self.mock_command_show_result.call_args_list == [call(result=result)]
        assert cmd_result.exit_code == result.return_code


@pytest.mark.usefixtures("mock_click_echo")
class TestCommandShowResult:  # pylint: disable=too-few-public-methods
    """Tests for clint.cli.command.Command.show_result method."""

    mock_click_echo: MagicMock

    results = [
        Result(operation="test", base_error_code=0),
        Result(operation="test", base_error_code=0).add_action(
            action="no_error", message="message", is_error=False
        ),
        Result(operation="test", base_error_code=0)
        .add_action(action="error", message="message", is_error=True)
        .add_action(action="no_error", message="message", is_error=False),
        Result(operation="test", base_error_code=0)
        .add_action(action="no_error", message="message", is_error=False)
        .add_action(action="error", message="message", is_error=True)
        .add_action(action="no_error_2", message="message", is_error=False),
    ]

    @pytest.mark.parametrize("result", results)
    def test_valid_invocation(self, result):
        """Test invocation with valid call."""
        self.mock_click_echo.reset_mock()
        Command.show_result(result=result)
        calls = []
        for action, message in result.actions.items():
            calls.append(call(f"{action}: {message}"))
        assert self.mock_click_echo.call_args_list == calls
