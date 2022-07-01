"""Tests for clint.validator module."""
# pylint: disable=too-many-arguments
from unittest.mock import MagicMock

import pytest

from clint.old_validator import conventional_commit_validator

from .validator.conftest import INVALID_DATA, VALID_DATA


@pytest.mark.usefixtures("mock_cc_get_commit_msg", "mock_sys_exit")
class TestConventionalCommitValidator:
    """Tests for clint.validator.conventional_commit_validator function."""

    mock_cc_get_commit_msg: MagicMock
    mock_sys_exit: MagicMock

    @pytest.mark.parametrize("c_type", VALID_DATA["types"])
    @pytest.mark.parametrize("scope", VALID_DATA["scopes"])
    @pytest.mark.parametrize("breaking", VALID_DATA["breaking_changes"])
    @pytest.mark.parametrize("body", VALID_DATA["bodies"])
    @pytest.mark.parametrize("footer", VALID_DATA["footers"])
    def test_correct_msg(self, c_type, scope, breaking, body, footer, sentence):
        """Test that all correct messages pass the validation."""
        msg = f"{c_type}{scope}{breaking}: {sentence}{body}{footer}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_not_called()

    @pytest.mark.parametrize("trailing", ["", ": "])
    def test_without_description(self, trailing):
        """Test that messages without description fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{VALID_DATA['types'][0]}{trailing}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("c_type", INVALID_DATA["types"])
    def test_invalid_type(self, c_type, sentence):
        """Test that messages with invalid type fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{c_type}: {sentence}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("scope", INVALID_DATA["scopes"])
    def test_invalid_scopes(self, scope, sentence):
        """Test that messages with invalid scope fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{VALID_DATA['types'][0]}{scope}: {sentence}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("body", INVALID_DATA["bodies"])
    def test_invalid_body(self, body, sentence):
        """Test that messages with invalid body fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{VALID_DATA['types'][0]}: {sentence}{body}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("footer", INVALID_DATA["footers"])
    def test_invalid_footer(self, footer, sentence):
        """Test that messages with invalid footer fails."""
        self.mock_sys_exit.reset_mock()
        msg = (
            f"{VALID_DATA['types'][0]}: {sentence}"
            + f"{VALID_DATA['footers'][-1]}{footer}"
        )
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("body", [b for b in VALID_DATA["bodies"] if b])
    @pytest.mark.parametrize("footer", [f for f in VALID_DATA["footers"] if f])
    def test_footer_before_body(self, body, footer, sentence):
        """Test that messages with footer before body paragraphs fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{VALID_DATA['types'][0]}: {sentence}{footer}{body}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)
