"""Test suite for generic test of CLint package."""
from unittest.mock import MagicMock

import pytest

import clint


@pytest.mark.usefixtures("metadata_current")
class TestClint:  # pylint: disable=too-few-public-methods
    """Tests for generic validations."""

    metadata_current: MagicMock

    def test_version(self):
        """Verify version for clint."""
        assert clint.__version__ == self.metadata_current["tool"]["poetry"]["version"]
