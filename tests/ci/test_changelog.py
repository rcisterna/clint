"""Test suite for special changelog validations in CI."""
from datetime import date
from pathlib import Path

import pytest


@pytest.mark.ci_changelog
@pytest.mark.usefixtures("changelog_dir", "metadata_current")
class TestChangelog:
    """Test for changelog."""

    changelog_dir: str
    metadata_current: dict

    def test_file_exists(self):
        """Verify that changelog file exists."""
        assert Path(self.changelog_dir).is_file()

    def test_contains_current_version(self):
        """Verify that changelog contains an entry for the current version."""
        with open(self.changelog_dir, mode="r", encoding="utf8") as changelog:
            changelog_content = changelog.read()

        version: str = self.metadata_current["tool"]["poetry"]["version"]
        today = date.today().isoformat()
        version_header = f"## [{version}] - {today}"
        assert version_header in changelog_content
