"""Test suite for CLI class."""
from unittest.mock import MagicMock, call

import pytest

from clint.cli.command import Command


@pytest.mark.usefixtures("mock_runner_validate", "mock_command_show_result")
class TestCommandEntrypoint:
    """Tests for clint.cli.command.Command.entrypoint method."""

    mock_runner_validate: MagicMock
    mock_command_show_result: MagicMock

    def test_valid_invocation(self, cli_runner, sentence):
        """Test valid invocation of the entrypoint."""
        self.mock_runner_validate.reset_mock()
        self.mock_command_show_result.reset_mock()
        msg = f"feat: {sentence}"
        result = cli_runner.invoke(Command.entrypoint, [msg])
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
