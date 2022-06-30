"""
Tests for clint.validator module.
"""
from unittest.mock import MagicMock

import pytest
from faker import Faker

from clint.old_validator import VALID_COMMIT_TYPES, conventional_commit_validator


@pytest.mark.usefixtures("mock_cc_get_commit_msg", "mock_sys_exit")
class TestConventionalCommitValidator:  # pylint: disable=too-many-arguments
    """Tests for clint.validator.conventional_commit_validator function."""

    mock_cc_get_commit_msg: MagicMock
    mock_sys_exit: MagicMock
    f = Faker()
    valid_data = {
        "types": list(VALID_COMMIT_TYPES),
        "scopes": [
            "",
            "(scope)",
            "(CamelScope)",
            "(dashed-scope)",
            "(numbered-scope-2)",
        ],
        "breaking_changes": ["", "!"],
        "bodies": [
            "",
            f"\n\n{f.paragraph(20)}",
            f"\n\n{f.sentence()}\n{f.sentence()}\n{f.sentence()}",
            f"\n\n{f.paragraph(10)}\n\n{f.paragraph(10)}",
        ],
        "footers": [
            "",
            f"\n\ntoken: {f.sentence()}",
            f"\n\nBREAKING CHANGE: {f.sentence()}",
            f"\n\nBREAKING-CHANGE: {f.sentence()}",
            f"\n\nmore-complex-token-1: {f.sentence()}",
            f"\n\nfirst-token: {f.sentence()}\n"
            + f"second-token: {f.sentence()}\n"
            + f"third-token: {f.sentence()}",
        ],
    }
    invalid_data = {
        "types": ["tets", "foo"],
        "scopes": [
            "[scope]",
            "scope",
        ],
        "bodies": [
            "\n\n\nToo many blank lines at beginning.",
            f"\n\n{f.paragraph(10)}\n\n\nToo many blank lines in the middle."
            + f"\n\n{f.paragraph(10)}",
        ],
        "footers": [
            f"\n\ntoken with space: {f.sentence()}",
            "\n\n\ntoken: Too many blank lines.",
        ],
    }

    @pytest.mark.parametrize("c_type", valid_data["types"])
    @pytest.mark.parametrize("scope", valid_data["scopes"])
    @pytest.mark.parametrize("breaking", valid_data["breaking_changes"])
    @pytest.mark.parametrize("body", valid_data["bodies"])
    @pytest.mark.parametrize("footer", valid_data["footers"])
    def test_correct_msg(
        self, c_type: str, scope: str, breaking: str, body: str, footer: str
    ):
        """Test that all correct messages pass the validation."""
        msg = f"{c_type}{scope}{breaking}: {self.f.sentence()}{body}{footer}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_not_called()

    @pytest.mark.parametrize("trailing", ["", ": "])
    def test_without_description(self, trailing: str):
        """Test that messages without description fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{self.valid_data['types'][0]}{trailing}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("c_type", invalid_data["types"])
    def test_invalid_type(self, c_type: str):
        """Test that messages with invalid type fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{c_type}: {self.f.sentence()}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("scope", invalid_data["scopes"])
    def test_invalid_scopes(self, scope: str):
        """Test that messages with invalid scope fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{self.valid_data['types'][0]}{scope}: {self.f.sentence()}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("body", invalid_data["bodies"])
    def test_invalid_body(self, body: str):
        """Test that messages with invalid body fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{self.valid_data['types'][0]}: {self.f.sentence()}{body}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("footer", invalid_data["footers"])
    def test_invalid_footer(self, footer: str):
        """Test that messages with invalid footer fails."""
        self.mock_sys_exit.reset_mock()
        msg = (
            f"{self.valid_data['types'][0]}: {self.f.sentence()}"
            + f"{self.valid_data['footers'][-1]}{footer}"
        )
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)

    @pytest.mark.parametrize("body", [b for b in valid_data["bodies"] if b])
    @pytest.mark.parametrize("footer", [f for f in valid_data["footers"] if f])
    def test_footer_before_body(self, body: str, footer: str):
        """Test that messages with footer before body paragraphs fails."""
        self.mock_sys_exit.reset_mock()
        msg = f"{self.valid_data['types'][0]}: {self.f.sentence()}{footer}{body}"
        self.mock_cc_get_commit_msg.return_value = msg
        conventional_commit_validator()
        self.mock_sys_exit.assert_called_once_with(1)
