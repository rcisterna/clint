"""Configuration for validator tests."""
import pytest
from faker import Faker

from clint.validator import Subject

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
            "",
            f"{faker.paragraph(20)}",
            f"{faker.sentence()}\n{faker.sentence()}\n{faker.sentence()}",
            f"{faker.paragraph(10)}\n{faker.paragraph(10)}",
        ]
    },
    "footer": {
        "tokens": [
            "token",
            "composed-token",
            "Token",
            "BREAKING CHANGE",
            "BREAKING-CHANGE",
            "Dashed-token",
            "Numbered-token-2",
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
        "texts": [],
    },
    "footer": {
        "tokens": ["token with space"],
        "separators": [":\t", "\t#"],
    },
}


@pytest.fixture
def subject() -> Subject:
    """Fixture to create dummy subject."""
    return Subject(c_type="", scope="", breaking="", separator="", description="")
