"""Configuration for general tests."""
import pytest
from faker import Faker

from .ci.conftest import metadata_current  # pylint: disable=unused-import

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
