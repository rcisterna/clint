"""Test suite for CLI class."""
from unittest.mock import MagicMock, call

import pytest

from clint.cli.command import Command
from clint.result import Result


@pytest.mark.usefixtures(
    "mock_runner_validate",
    "mock_runner_change_hook_handler",
    "mock_runner_help",
    "mock_command_show_result",
)
class TestCommandEntrypoint:
    """Tests for clint.cli.command.Command.entrypoint method."""

    mock_runner_validate: MagicMock
    mock_runner_change_hook_handler: MagicMock
    mock_runner_help: MagicMock
    mock_command_show_result: MagicMock

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
        self.mock_runner_change_hook_handler.reset_mock()
        self.mock_runner_help.reset_mock()
        self.mock_command_show_result.reset_mock()
        cmd_result = cli_runner.invoke(Command.entrypoint, [sentence])
        assert self.mock_runner_validate.call_args_list == [call(message=sentence)]
        assert not self.mock_runner_change_hook_handler.called
        assert not self.mock_runner_help.called
        assert self.mock_command_show_result.call_args_list == [call(result=result)]
        assert cmd_result.exit_code == result.return_code

    @pytest.mark.parametrize("result", results)
    def test_with_pipe_message(self, cli_runner, sentence, result):
        """Test invocation of the entrypoint with message from shell pipe."""
        self.mock_runner_validate.reset_mock()
        self.mock_runner_validate.return_value = result
        self.mock_runner_change_hook_handler.reset_mock()
        self.mock_runner_help.reset_mock()
        self.mock_command_show_result.reset_mock()
        cmd_result = cli_runner.invoke(Command.entrypoint, input=f'{sentence}\n')
        assert self.mock_runner_validate.call_args_list == [call(message=sentence)]
        assert not self.mock_runner_change_hook_handler.called
        assert not self.mock_runner_help.called
        assert self.mock_command_show_result.call_args_list == [call(result=result)]
        assert cmd_result.exit_code == result.return_code

    @pytest.mark.parametrize("result", results)
    def test_with_file(self, cli_runner, sentence, result):
        """Test invocation of the entrypoint with file."""
        self.mock_runner_validate.reset_mock()
        self.mock_runner_validate.return_value = result
        self.mock_runner_change_hook_handler.reset_mock()
        self.mock_runner_help.reset_mock()
        self.mock_command_show_result.reset_mock()
        with cli_runner.isolated_filesystem():
            filename = "example.txt"
            with open(filename, "w", encoding="utf8") as temp_file:
                temp_file.write(sentence)
            cmd_result = cli_runner.invoke(Command.entrypoint, ["--file", filename])
        assert self.mock_runner_validate.call_args_list == [call(message=sentence)]
        assert not self.mock_runner_change_hook_handler.called
        assert not self.mock_runner_help.called
        assert self.mock_command_show_result.call_args_list == [call(result=result)]
        assert cmd_result.exit_code == result.return_code

    def test_empty_invocation(self, cli_runner):
        """Test invocation of the entrypoint with no arguments."""
        self.mock_runner_validate.reset_mock()
        self.mock_runner_change_hook_handler.reset_mock()
        self.mock_runner_help.reset_mock()
        self.mock_command_show_result.reset_mock()
        cmd_result = cli_runner.invoke(Command.entrypoint)
        assert not self.mock_runner_validate.called
        assert not self.mock_runner_change_hook_handler.called
        assert self.mock_runner_help.call_args_list == [call()]
        assert self.mock_command_show_result.call_args_list == [
            call(result=self.mock_runner_help.return_value)
        ]
        assert cmd_result.exit_code == 0

    @pytest.mark.parametrize("hook_flag", ["--enable-hook", "--disable-hook"])
    def test_hook(self, hook_flag, cli_runner):
        """Test invocation of the entrypoint for git hook."""
        self.mock_runner_validate.reset_mock()
        self.mock_runner_change_hook_handler.reset_mock()
        self.mock_runner_help.reset_mock()
        self.mock_command_show_result.reset_mock()
        hook_handler_calls = [call(is_enabling=bool(hook_flag == "--enable-hook"))]
        cmd_result = cli_runner.invoke(Command.entrypoint, [hook_flag])
        assert not self.mock_runner_validate.called
        assert self.mock_runner_change_hook_handler.call_args_list == hook_handler_calls
        assert not self.mock_runner_help.called
        assert self.mock_command_show_result.called
        assert cmd_result.exit_code == 0


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
