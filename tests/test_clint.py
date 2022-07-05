"""Test suite for generic test of CLint package."""
from clint import __version__


def test_version():
    """Verify version for clint."""
    assert __version__ == "0.1.0"
