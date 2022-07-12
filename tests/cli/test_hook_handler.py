"""Test suite for HookHandler class."""
from unittest.mock import MagicMock, call

import pytest

from clint.cli.exceptions import HookException
from clint.cli.hook_handler import HookHandler


@pytest.mark.usefixtures("mock_hook_os_getcwd", "valid_path")
class TestHookHandlerGetRepoRoot:
    """Tests for clint.cli.hook_handler.HookHandler._get_repo_root method."""

    mock_hook_os_getcwd: MagicMock
    valid_path: str

    def test_inside_repo(self, mock_hook_path_is_dir):
        """Test invocation in valid git directory."""
        self.mock_hook_os_getcwd.reset_mock()
        self.mock_hook_os_getcwd.return_value = self.valid_path
        mock_hook_path_is_dir.return_value = True
        hook_handler = HookHandler()
        assert hook_handler.path == self.valid_path

    def test_outside_repo(self, mock_hook_path_is_dir):
        """Test invocation in a non git directory."""
        self.mock_hook_os_getcwd.reset_mock()
        self.mock_hook_os_getcwd.return_value = self.valid_path
        mock_hook_path_is_dir.return_value = False
        with pytest.raises(HookException) as exception:
            HookHandler()
        assert exception.value.args == ("Not in a git repository.",)


@pytest.mark.usefixtures("mock_hook_get_repo_root")
class TestHookHandlerIsEnabled:
    """Tests for clint.cli.hook_handler.HookHandler.is_enabled property."""

    def test_no_hooks_file(self, mock_hook_path_is_file):
        """Test property if no hooks file."""
        mock_hook_path_is_file.return_value = False
        hook_handler = HookHandler()
        assert not hook_handler.is_enabled

    def test_command_in_hooks_file(self, mock_hook_path_is_file, mocker):
        """Test property if no hooks file."""
        mock_hook_path_is_file.return_value = True
        mocked_open = mocker.mock_open(read_data=HookHandler.COMMAND)
        mocker.patch("clint.cli.hook_handler.open", mocked_open)
        hook_handler = HookHandler()
        assert hook_handler.is_enabled

    def test_command_not_in_hooks_file(self, mock_hook_path_is_file, mocker, sentence):
        """Test property if no hooks file."""
        mock_hook_path_is_file.return_value = True
        mocked_open = mocker.mock_open(read_data=sentence)
        mocker.patch("clint.cli.hook_handler.open", mocked_open)
        hook_handler = HookHandler()
        assert not hook_handler.is_enabled


@pytest.mark.usefixtures(
    "mock_hook_get_repo_root", "mock_hook_is_enabled", "mock_hook_os_chmod"
)
class TestHookHandlerEnable:
    """Tests for clint.cli.hook_handler.HookHandler.enable method."""

    mock_hook_is_enabled: MagicMock
    mock_hook_os_chmod: MagicMock

    def test_already_enabled(self):
        """Test invocation if hook is already enabled."""
        self.mock_hook_is_enabled.return_value = True
        hook_handler = HookHandler()
        result = hook_handler.enable()
        assert result.return_code == HookHandler.OPERATION_BASE_ERROR_CODE + 1
        assert result.actions == {
            "Enable hook": "Hook already enabled in this repository."
        }

    def test_no_hooks_file(self, mock_hook_path_is_file, mocker):
        """Test invocation if no hooks file."""
        self.mock_hook_os_chmod.reset_mock()
        self.mock_hook_is_enabled.return_value = False
        mock_hook_path_is_file.return_value = False
        mocked_open = mocker.mock_open()
        mocker.patch("clint.cli.hook_handler.open", mocked_open)
        hook_handler = HookHandler()
        result = hook_handler.enable()
        assert result.return_code == 0
        assert result.actions == {
            "Enable hook": f"Hook enabled at {hook_handler.hook_filepath}"
        }
        assert mocked_open.call_args_list == [
            call(hook_handler.hook_filepath, mode="w", encoding="utf8"),
            call(hook_handler.hook_filepath, mode="a", encoding="utf8"),
        ]
        assert self.mock_hook_os_chmod.call_args_list == [
            call(hook_handler.hook_filepath, 0o755)
        ]
        mocked_file = mocked_open()
        assert mocked_file.write.call_args_list == [call(f"{HookHandler.COMMAND}\n")]

    def test_add_hook(self, mock_hook_path_is_file, mocker):
        """Test invocation if no hooks file."""
        self.mock_hook_os_chmod.reset_mock()
        self.mock_hook_is_enabled.return_value = False
        mock_hook_path_is_file.return_value = True
        mocked_open = mocker.mock_open()
        mocker.patch("clint.cli.hook_handler.open", mocked_open)
        hook_handler = HookHandler()
        result = hook_handler.enable()
        assert result.return_code == 0
        assert result.actions == {
            "Enable hook": f"Hook enabled at {hook_handler.hook_filepath}"
        }
        assert mocked_open.call_args_list == [
            call(hook_handler.hook_filepath, mode="a", encoding="utf8")
        ]
        assert not self.mock_hook_os_chmod.called
        mocked_file = mocked_open()
        assert mocked_file.write.call_args_list == [call(f"{HookHandler.COMMAND}\n")]


@pytest.mark.usefixtures(
    "mock_hook_get_repo_root", "mock_hook_is_enabled", "mock_hook_os_remove"
)
class TestHookHandlerDisable:
    """Tests for clint.cli.hook_handler.HookHandler.disable method."""

    mock_hook_is_enabled: MagicMock
    mock_hook_os_remove: MagicMock

    def test_already_disabled(self):
        """Test invocation if hook is already disabled."""
        self.mock_hook_is_enabled.return_value = False
        hook_handler = HookHandler()
        result = hook_handler.disable()
        assert result.return_code == HookHandler.OPERATION_BASE_ERROR_CODE + 1
        assert result.actions == {
            "Disable hook": "Hook it is not enabled in this repository."
        }

    def test_no_hooks_file(self, mocker, faker):
        """Test invocation if there are many hooks."""
        self.mock_hook_os_remove.reset_mock()
        self.mock_hook_is_enabled.return_value = True
        p_hook = faker.sentence()
        n_hook = faker.sentence()
        mocked_open = mocker.mock_open(
            read_data=f"{p_hook}\n{HookHandler.COMMAND}\n{n_hook}\n"
        )
        mocker.patch("clint.cli.hook_handler.open", mocked_open)
        hook_handler = HookHandler()
        result = hook_handler.disable()
        assert result.return_code == 0
        assert result.actions == {
            "Disable hook": f"Hook disabled at {hook_handler.hook_filepath}"
        }
        assert mocked_open.call_args_list == [
            call(hook_handler.hook_filepath, mode="r", encoding="utf8"),
            call(hook_handler.hook_filepath, mode="w", encoding="utf8"),
        ]
        assert not self.mock_hook_os_remove.called
        mocked_file = mocked_open()
        assert mocked_file.write.call_args_list == [call(f"{p_hook}\n{n_hook}\n")]

    def test_remove_hook(self, mocker):
        """Test invocation if the only hook is clint."""
        self.mock_hook_os_remove.reset_mock()
        self.mock_hook_is_enabled.return_value = True
        mocked_open = mocker.mock_open(read_data=f"{HookHandler.COMMAND}\n")
        mocker.patch("clint.cli.hook_handler.open", mocked_open)
        hook_handler = HookHandler()
        result = hook_handler.disable()
        assert result.return_code == 0
        assert result.actions == {
            "Disable hook": f"Hook disabled at {hook_handler.hook_filepath}"
        }
        assert mocked_open.call_args_list == [
            call(hook_handler.hook_filepath, mode="r", encoding="utf8")
        ]
        assert self.mock_hook_os_remove.call_args_list == [
            call(hook_handler.hook_filepath)
        ]
