"""Configuration for general tests."""
import pytest
from click.testing import CliRunner
from faker import Faker

from clint import validator

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


@pytest.fixture(scope="class")
def mock_validate_commit_message(request, class_mocker):
    """Fixture to patch cli.CLI.validate_commit_message method."""
    request.cls.mock_validate_commit_message = class_mocker.patch(
        "clint.cli.CLI.validate_commit_message"
    )


@pytest.fixture(scope="class")
def mock_commit_generate(request, class_mocker):
    """Fixture to patch clint.cli.validator.Commit.generate method."""
    request.cls.mock_commit_generate = class_mocker.patch(
        "clint.cli.validator.Commit.generate", return_value=validator.Commit("")
    )


@pytest.fixture(scope="class")
def mock_commit_validate(request, class_mocker):
    """Fixture to patch clint.cli.validator.Commit.validate method."""
    request.cls.mock_commit_validate = class_mocker.patch(
        "clint.cli.validator.Commit.validate", return_value=True
    )


@pytest.fixture(scope="class")
def mock_click_echo(request, class_mocker):
    """Fixture to patch clint.cli.validator.Commit.validate method."""
    request.cls.mock_click_echo = class_mocker.patch("click.echo")


@pytest.fixture
def clean_commit_mocks(request: pytest.FixtureRequest):
    """Fixture to reset mock_subject_validate and mock_paragraph_validate."""
    request.cls.mock_commit_generate.reset_mock()
    request.cls.mock_commit_generate.side_effect = None
    request.cls.mock_commit_validate.reset_mock()
    request.cls.mock_commit_validate.side_effect = None
    request.cls.mock_click_echo.reset_mock()


@pytest.fixture
def sentence() -> str:
    """Fixture to get a faker sentence."""
    return faker.sentence()


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture to get a CliRunner instance."""
    return CliRunner()
