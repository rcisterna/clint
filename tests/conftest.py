"""Configuration for general tests."""
import pytest
from pytest_mock import MockerFixture


@pytest.fixture(scope="class")
def mock_cc_get_commit_msg(request: pytest.FixtureRequest, class_mocker: MockerFixture):
    """Fixture to patch clint.validator.get_commit_msg function."""
    request.cls.mock_cc_get_commit_msg = class_mocker.patch(
        "clint.validator.get_commit_msg"
    )


@pytest.fixture(scope="class")
def mock_sys_exit(request: pytest.FixtureRequest, class_mocker: MockerFixture):
    """Fixture to patch sys.exit function."""
    request.cls.mock_sys_exit = class_mocker.patch("sys.exit")
