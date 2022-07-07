"""Configuration for general tests."""
import os.path

import pytest
import toml
import urllib3
from faker import Faker

faker = Faker()


@pytest.fixture(scope="class")
def mock_cc_get_commit_msg(request, class_mocker):
    """Fixture to patch clint.validator.get_commit_msg function."""
    request.cls.mock_cc_get_commit_msg = class_mocker.patch(
        "clint.old_validator.get_commit_msg"
    )


@pytest.fixture(scope="class")
def mock_sys_exit(request, class_mocker):
    """Fixture to patch sys.exit function."""
    request.cls.mock_sys_exit = class_mocker.patch("sys.exit")


@pytest.fixture
def sentence() -> str:
    """Fixture to get a faker sentence."""
    return faker.sentence()


@pytest.fixture
def clint_metadata(pytestconfig) -> dict:
    """Fixture to get the CLint metadata as dictionary."""
    pyproject_path = os.path.join(pytestconfig.rootpath, "pyproject.toml")
    with open(pyproject_path, mode="r", encoding="utf8") as pyproject:
        metadata = toml.load(pyproject)
    return metadata


@pytest.fixture
def clint_main_metadata() -> dict:
    """Fixture to get the CLint metadata as dictionary."""
    url = "https://raw.githubusercontent.com/rcisterna/clint/main/pyproject.toml"
    http = urllib3.PoolManager()
    with http.request("GET", url, preload_content=False) as response:
        pyproject_str = response.data.decode("utf8")
    return toml.loads(pyproject_str)
