"""Test suite for special version validations in CI."""
import pytest


@pytest.mark.ci_version
@pytest.mark.usefixtures("metadata_current", "metadata_production")
class TestVersion:
    """Test for version."""

    metadata_current: dict
    metadata_production: dict

    def test_is_different(self):
        """Verify current clint version is distinct to production version."""
        version_current: str = self.metadata_current["tool"]["poetry"]["version"]
        version_production: str = self.metadata_production["tool"]["poetry"]["version"]
        assert version_current != version_production

    def test_current_is_higher(self):
        """Verify current clint version is higher than production version."""
        version_current: str = self.metadata_current["tool"]["poetry"]["version"]
        version_production: str = self.metadata_production["tool"]["poetry"]["version"]
        curr_versions = tuple(int(v) for v in version_current.split("."))
        main_versions = tuple(int(v) for v in version_production.split("."))
        for curr_version, main_version in zip(curr_versions, main_versions):
            assert curr_version >= main_version
            if curr_version > main_version:
                break
