"""Configuration for validator tests."""
import pytest
from faker import Faker

from clint.validator import Subject

faker = Faker()

VALID_DATA = {
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
    "bodies": [
        "",
        f"\n\n{faker.paragraph(20)}",
        f"\n\n{faker.sentence()}\n{faker.sentence()}\n{faker.sentence()}",
        f"\n\n{faker.paragraph(10)}\n\n{faker.paragraph(10)}",
    ],
    "footers": [
        "",
        f"\n\ntoken: {faker.sentence()}",
        f"\n\nBREAKING CHANGE: {faker.sentence()}",
        f"\n\nBREAKING-CHANGE: {faker.sentence()}",
        f"\n\nmore-complex-token-1: {faker.sentence()}",
        f"\n\nfirst-token: {faker.sentence()}\n"
        + f"second-token: {faker.sentence()}\n"
        + f"third-token: {faker.sentence()}",
    ],
}

INVALID_DATA = {
    "types": ["", "tets", "foo", "Chore"],
    "scopes": ["[scope]", "scope", "(scope]", "()"],
    "separators": ["", ":\t", ":  "],
    "descriptions": [""],
    "bodies": [
        "\n\n\nToo many blank lines at beginning.",
        f"\n\n{faker.paragraph(10)}\n\n\nToo many blank lines in the middle."
        + f"\n\n{faker.paragraph(10)}",
    ],
    "footers": [
        f"\n\ntoken with space: {faker.sentence()}",
        "\n\n\ntoken: Too many blank lines.",
    ],
}


@pytest.fixture
def subject() -> Subject:
    """Fixture to create dummy subject."""
    return Subject(c_type="", scope="", breaking="", separator="", description="")
