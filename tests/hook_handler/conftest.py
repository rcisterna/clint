"""Configuration for hook handler tests."""
import os
from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope="class")
def mock_hook_os_getcwd(request, class_mocker):
    """Fixture to patch os.getcwd function at clint.hook_handler.hook_handler."""
    request.cls.mock_hook_os_getcwd = class_mocker.patch(
        "clint.hook_handler.hook_handler.os.getcwd"
    )


@pytest.fixture(scope="class")
def mock_hook_os_chmod(request, class_mocker):
    """Fixture to patch os.chmod function at clint.hook_handler.hook_handler."""
    request.cls.mock_hook_os_chmod = class_mocker.patch(
        "clint.hook_handler.hook_handler.os.chmod"
    )


@pytest.fixture(scope="class")
def mock_hook_os_remove(request, class_mocker):
    """Fixture to patch os.remove function at clint.hook_handler.hook_handler."""
    request.cls.mock_hook_os_remove = class_mocker.patch(
        "clint.hook_handler.hook_handler.os.remove"
    )


@pytest.fixture
def mock_hook_path_is_dir(mocker) -> MagicMock:
    """Fixture to patch Path.is_dir method at clint.hook_handler."""
    return mocker.patch("clint.hook_handler.hook_handler.Path.is_dir")


@pytest.fixture
def mock_hook_path_is_file(mocker) -> MagicMock:
    """Fixture to patch Path.is_file method at clint.hook_handler."""
    return mocker.patch("clint.hook_handler.hook_handler.Path.is_file")


@pytest.fixture(scope="class")
def valid_path(request):
    """Fixture to get a valid (nonexistent) path."""
    request.cls.valid_path = os.path.abspath(os.path.join(os.sep, "valid", "path"))


@pytest.fixture(scope="class")
def mock_hook_get_repo_root(
    request, class_mocker, valid_path
):  # pylint: disable=unused-argument,redefined-outer-name
    """Fixture for cli.hook_handler.HookHandler._get_repo_root method."""
    request.cls.mock_hook_get_repo_root = class_mocker.patch(
        "clint.hook_handler.hook_handler.HookHandler._get_repo_root",
        return_value=request.cls.valid_path,
    )


@pytest.fixture(scope="class")
def mock_hook_is_enabled(request, class_mocker):
    """Fixture for cli.hook_handler.HookHandler.is_enabled property."""
    request.cls.mock_hook_is_enabled = class_mocker.PropertyMock
    class_mocker.patch(
        "clint.hook_handler.hook_handler.HookHandler.is_enabled",
        new_callable=request.cls.mock_hook_is_enabled,
    )
