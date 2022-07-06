"""Test suite for special validations in CI."""
import pytest


@pytest.mark.ci_version
def test_version_against_main(clint_metadata, clint_main_metadata):
    """Verify current clint version against main version."""
    curr_full_version: str = clint_metadata["tool"]["poetry"]["version"]
    main_full_version: str = clint_main_metadata["tool"]["poetry"]["version"]

    # Validate that the versions are different
    assert curr_full_version != main_full_version

    # Validate that the current (curr) version is higher than the main version
    curr_versions = tuple(int(v) for v in curr_full_version.split("."))
    main_versions = tuple(int(v) for v in main_full_version.split("."))
    for curr_version, main_version in zip(curr_versions, main_versions):
        assert curr_version >= main_version
        if curr_version > main_version:
            break
