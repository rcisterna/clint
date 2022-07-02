"""Configuration for validator tests."""
import pytest
from faker import Faker
from pytest_mock import MockerFixture

from clint.validator import Commit, Footer, Paragraph, Subject

faker = Faker()

VALID_DATA = {
    "subject": {
        "types": list(Subject.VALID_COMMIT_TYPES),
        "scopes": [
            "",
            "(scope)",
            "(CamelScope)",
            "(dashed-scope)",
            "(numbered-scope-2)",
        ],
        "breaking_changes": ["", "!"],
        "separators": [": "],
    },
    "body": {
        "texts": [
            f"{faker.paragraph(10)}",
            f"{faker.paragraph(20)}",
            f"token-1: {faker.sentence()}\ntoken-2 #{faker.sentence()}",
        ]
    },
    "footer": {
        "tokens": [
            "token",
            "dashed-token",
            "CamelToken",
            "Camel-Dash-Token",
            "numbered-token-2",
            "BREAKING CHANGE",
            "BREAKING-CHANGE",
        ],
        "separators": [": ", " #"],
    },
}

INVALID_DATA = {
    "subject": {
        "types": ["", "tets", "foo", "Chore"],
        "scopes": ["[scope]", "scope", "(scope]", "()"],
        "separators": ["", ":\t", ":  "],
        "descriptions": [""],
    },
    "body": {
        "texts": [
            "",
            f"{faker.sentence()}\n{faker.sentence()}\n{faker.sentence()}",
            f"{faker.paragraph(10)}\n{faker.paragraph(10)}",
            f"impure-1: {faker.sentence()}\n"
            + f"{faker.sentence()}\n"
            + f"impure-2 #{faker.sentence()}",
        ],
    },
    "footer": {
        "tokens": ["", "token with space"],
        "separators": ["", ":\t", "\t#"],
        "descriptions": [""],
    },
}


@pytest.fixture
def subject() -> Subject:
    """Fixture to create dummy subject."""
    return Subject(c_type="", scope="", breaking="", separator="", description="")


@pytest.fixture
def footer() -> Footer:
    """Fixture to create dummy footer."""
    return Footer(token="", separator="", description="")


@pytest.fixture
def paragraph() -> Paragraph:
    """Fixture to create dummy paragraph."""
    return Paragraph(text="")


@pytest.fixture
def commit() -> Commit:
    """Fixture to create dummy commit."""
    return Commit(text="")


@pytest.fixture(scope="class")
def mock_subject_validate(request: pytest.FixtureRequest, class_mocker: MockerFixture):
    """Fixture to patch clint.validator.subject.Subject.validate method."""
    request.cls.mock_subject_validate = class_mocker.patch(
        "clint.validator.subject.Subject.validate", return_value=True
    )


@pytest.fixture(scope="class")
def mock_paragraph_validate(
    request: pytest.FixtureRequest, class_mocker: MockerFixture
):
    """Fixture to patch clint.validator.paragraph.Paragraph.validate method."""
    request.cls.mock_paragraph_validate = class_mocker.patch(
        "clint.validator.paragraph.Paragraph.validate", return_value=True
    )


@pytest.fixture
def mock_clean_validations(request: pytest.FixtureRequest):
    """Fixture to reset mock_subject_validate and mock_paragraph_validate."""
    request.cls.mock_subject_validate.reset_mock()
    request.cls.mock_subject_validate.side_effect = None
    request.cls.mock_paragraph_validate.reset_mock()
    request.cls.mock_paragraph_validate.side_effect = None
