"""Test suite for generic test of CLint package."""
import clint


def test_version(clint_metadata):
    """Verify version for clint."""
    assert clint.__version__ == clint_metadata["tool"]["poetry"]["version"]
