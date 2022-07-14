"""Configuration for CI tests."""
import os.path

import pytest
import toml
import urllib3


@pytest.fixture(scope="class")
def metadata_current(request, pytestconfig) -> None:
    """Fixture to get the CLint metadata as dictionary."""
    pyproject_path = os.path.join(pytestconfig.rootpath, "pyproject.toml")
    with open(pyproject_path, mode="r", encoding="utf8") as pyproject:
        metadata = toml.load(pyproject)
    request.cls.metadata_current = metadata


@pytest.fixture(scope="class")
def metadata_production(request) -> None:
    """Fixture to get the CLint metadata as dictionary."""
    url = "https://raw.githubusercontent.com/rcisterna/clint/main/pyproject.toml"
    http = urllib3.PoolManager()
    with http.request("GET", url, preload_content=False) as response:
        pyproject_str = response.data.decode("utf8")
    request.cls.metadata_production = toml.loads(pyproject_str)
