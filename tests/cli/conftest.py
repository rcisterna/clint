"""Tests suite for CLI classes."""
import os
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

from clint import validator


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture to get a CliRunner instance."""
    return CliRunner()


@pytest.fixture(scope="class")
def hook_handler_methods(request, class_mocker):
    """Fixture to patch cli.hook_handler.HookHandler methods."""
    request.cls.mock_hook_get_repo_root = class_mocker.patch(
        "clint.cli.hook_handler.HookHandler._get_repo_root"
    )
    request.cls.mock_hook_enable = class_mocker.patch(
        "clint.cli.hook_handler.HookHandler.enable"
    )
    request.cls.mock_hook_disable = class_mocker.patch(
        "clint.cli.hook_handler.HookHandler.disable"
    )


@pytest.fixture
def clean_hook_handler_methods(request: pytest.FixtureRequest):
    """Fixture to reset hook_handler_methods fixture mocks."""
    request.cls.mock_hook_get_repo_root.reset_mock()
    request.cls.mock_hook_enable.reset_mock()
    request.cls.mock_hook_disable.reset_mock()
    request.cls.mock_hook_get_repo_root.side_effect = None
    request.cls.mock_hook_enable.side_effect = None
    request.cls.mock_hook_disable.side_effect = None


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


@pytest.fixture
def clean_commit_mocks(request: pytest.FixtureRequest):
    """Fixture to reset mock_subject_validate and mock_paragraph_validate."""
    request.cls.mock_commit_generate.reset_mock()
    request.cls.mock_commit_generate.side_effect = None
    request.cls.mock_commit_validate.reset_mock()
    request.cls.mock_commit_validate.side_effect = None


@pytest.fixture(scope="class")
def mock_click_echo(request, class_mocker):
    """Fixture to patch clint.validator.Commit.validate method."""
    request.cls.mock_click_echo = class_mocker.patch("click.echo")


@pytest.fixture(scope="class")
def mock_hook_os_getcwd(request, class_mocker):
    """Fixture to patch os.getcwd function at clint.cli.hook_handler."""
    request.cls.mock_hook_os_getcwd = class_mocker.patch(
        "clint.cli.hook_handler.os.getcwd"
    )


@pytest.fixture(scope="class")
def mock_hook_os_chmod(request, class_mocker):
    """Fixture to patch os.chmod function at clint.cli.hook_handler."""
    request.cls.mock_hook_os_chmod = class_mocker.patch(
        "clint.cli.hook_handler.os.chmod"
    )


@pytest.fixture(scope="class")
def mock_hook_os_remove(request, class_mocker):
    """Fixture to patch os.remove function at clint.cli.hook_handler."""
    request.cls.mock_hook_os_remove = class_mocker.patch(
        "clint.cli.hook_handler.os.remove"
    )


@pytest.fixture(scope="class")
def mock_hook_get_repo_root(
    request, class_mocker, valid_path
):  # pylint: disable=unused-argument,redefined-outer-name
    """Fixture for cli.hook_handler.HookHandler._get_repo_root method."""
    request.cls.mock_hook_get_repo_root = class_mocker.patch(
        "clint.cli.hook_handler.HookHandler._get_repo_root",
        return_value=request.cls.valid_path,
    )


@pytest.fixture(scope="class")
def mock_hook_is_enabled(request, class_mocker):
    """Fixture for cli.hook_handler.HookHandler.is_enabled property."""
    request.cls.mock_hook_is_enabled = class_mocker.PropertyMock
    class_mocker.patch(
        "clint.cli.hook_handler.HookHandler.is_enabled",
        new_callable=request.cls.mock_hook_is_enabled,
    )


@pytest.fixture(scope="class")
def valid_path(request):
    """Fixture to get a valid (nonexistent) path."""
    request.cls.valid_path = os.path.abspath(os.path.join(os.sep, "valid", "path"))


@pytest.fixture
def mock_hook_path_is_dir(mocker) -> MagicMock:
    """Fixture to patch Path.is_dir method at clint.cli.hook_handler."""
    return mocker.patch("clint.cli.hook_handler.Path.is_dir")


@pytest.fixture
def mock_hook_path_is_file(mocker) -> MagicMock:
    """Fixture to patch Path.is_file method at clint.cli.hook_handler."""
    return mocker.patch("clint.cli.hook_handler.Path.is_file")
