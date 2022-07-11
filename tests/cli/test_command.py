"""Test suite for CLI class."""
from unittest.mock import MagicMock, call

import pytest

from clint.cli.command import Command
from clint.cli.exceptions import HookException


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

    def test_with_message(self, cli_runner, sentence):
        """Test invocation of the entrypoint with message."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        msg = f"feat: {sentence}"
        result = cli_runner.invoke(Command.entrypoint, [msg])
        assert self.mock_runner_validate.call_args_list == [call(message=msg)]
        assert self.mock_command_show_result.call_count == 1
        assert not result.exception
        assert result.exit_code == 0

    def test_with_file(self, cli_runner, sentence):
        """Test invocation of the entrypoint with file."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        msg = f"feat: {sentence}"
        with cli_runner.isolated_filesystem():
            filename = "example.txt"
            with open(filename, "w", encoding="utf8") as temp_file:
                temp_file.write(msg)
            result = cli_runner.invoke(Command.entrypoint, ["--file", filename])
        assert self.mock_runner_validate.call_args_list == [call(message=msg)]
        assert self.mock_command_show_result.call_count == 1
        assert not result.exception
        assert result.exit_code == 0

    def test_empty_invocation(self, cli_runner):
        """Test invocation of the entrypoint with no arguments."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        result = cli_runner.invoke(Command.entrypoint)
        assert not self.mock_runner_validate.called
        assert not self.mock_command_show_result.called
        assert result.exit_code == 0

    @pytest.mark.parametrize("hook_flag", ["--enable-hook", "--disable-hook"])
    def test_hook_outside_repo(
        self, hook_flag, cli_runner, sentence, clean_hook_handler_methods
    ):
        """Test invocation of the entrypoint for git hook outside repo directory."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        self.mock_hook_get_repo_root.side_effect = HookException(sentence)
        result = cli_runner.invoke(Command.entrypoint, [hook_flag])
        assert self.mock_hook_get_repo_root.call_args_list == [call()]
        assert not self.mock_hook_enable.called
        assert not self.mock_hook_disable.called
        assert not self.mock_runner_validate.called
        assert self.mock_command_show_result.call_args_list == [call(result=sentence)]
        assert result.exit_code == 0

    def test_hook_enable(self, cli_runner, sentence, clean_hook_handler_methods):
        """Test invocation of the entrypoint to enable git hook."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        self.mock_hook_enable.return_value = sentence
        result = cli_runner.invoke(Command.entrypoint, ["--enable-hook"])
        assert self.mock_hook_get_repo_root.call_args_list == [call()]
        assert self.mock_hook_enable.call_args_list == [call()]
        assert not self.mock_hook_disable.called
        assert not self.mock_runner_validate.called
        assert self.mock_command_show_result.call_args_list == [call(result=sentence)]
        assert result.exit_code == 0

    def test_hook_disable(self, cli_runner, sentence, clean_hook_handler_methods):
        """Test invocation of the entrypoint to disable git hook."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        self.mock_hook_disable.return_value = sentence
        result = cli_runner.invoke(Command.entrypoint, ["--disable-hook"])
        assert self.mock_hook_get_repo_root.call_args_list == [call()]
        assert not self.mock_hook_enable.called
        assert self.mock_hook_disable.call_args_list == [call()]
        assert not self.mock_runner_validate.called
        assert self.mock_command_show_result.call_args_list == [call(result=sentence)]
        assert result.exit_code == 0


@pytest.mark.usefixtures("mock_click_echo")
class TestCommandShowResult:  # pylint: disable=too-few-public-methods
    """Tests for clint.cli.command.Command.show_result method."""

    mock_click_echo: MagicMock

    def test_valid_invocation(self, sentence):
        """Test invocation with valid call."""
        self.mock_click_echo.reset_mock()
        result = Command.show_result(result=sentence)
        assert result is None
        assert self.mock_click_echo.call_args_list == [call(sentence)]
