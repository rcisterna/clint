#!/usr/bin/env python
"""
Conventional commits validator module
"""

import re
import sys
from typing import List

VALID_COMMIT_TYPES = {
    "build",
    "chore",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "revert",
    "style",
    "test",
}

PATTERN_COMMENTS = re.compile(r"^#.*\n?", flags=re.MULTILINE)
PATTERN_TRAILING_LINES = re.compile(r"\n*$")
PATTERN_HEADER = re.compile(
    r"^(?P<type>\w+)"
    + r"(?P<scope>\([\w\- :]+\))?"
    + r"(?P<breaking_change>!)?"
    + r": "
    + r"(?P<description>.+)$"
)
PATTERN_FOOTER = re.compile(
    r"^(?:(?P<token>[\w|-]+|BREAKING CHANGE)" + r": " + r"(?P<description>.+)\n?)+$"
)


def get_commit_msg() -> str:
    """
    Get the commit message, from file or from stdin stream.

    Returns
    -------
    str:
        The commit message.

    """
    # a file is passed as argument
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        with open(filepath, "r", encoding="utf-8") as file:
            commit_msg = file.read()
    # read stdin stream
    else:
        commit_msg = "".join(sys.stdin.readlines())
    commit_msg = PATTERN_COMMENTS.sub("", commit_msg)
    commit_msg = PATTERN_TRAILING_LINES.sub("", commit_msg)
    return commit_msg


def process_header(line: str, errors: List[str]) -> None:
    """
    Analyzes the header portion of the commit message.

    Parameters
    ----------
    line: str
        The header portion of the commit message.
    errors: list of str
        List containing the current errors.

    """
    match = PATTERN_HEADER.match(line)
    if match is None:
        errors.append(
            f"First line '{line}' does not match conventional commits specification"
        )
        return
    groups = match.groupdict()
    commit_type = groups["type"]
    if not commit_type.islower():
        errors.append(f"Type '{commit_type}' is not lowercase")
        return
    if commit_type not in VALID_COMMIT_TYPES:
        errors.append(f"Type '{commit_type}' is not a valid type")
        return


def process_paragraph(
    lines: str, footer_already_found: bool, errors: List[str]
) -> bool:
    """
    Analyzes a body or footer portion of the commit message.

    Parameters
    ----------
    lines: list of str
        A body or footer lines of the commit message.
    footer_already_found: bool, default=False
        Indicates if a footer was already found in another paragraph.
    errors: list of str
        List containing the current errors.

    Returns
    -------
    bool:
        True if a footer was found, False otherwise.

    """
    if lines.startswith("\n") or lines.endswith("\n"):
        errors.append("Too many new lines between paragraphs")
    lines = lines.strip()
    matches = PATTERN_FOOTER.match(lines)
    if matches:
        return True
    if not lines:
        errors.append("Empty paragraph")
    elif footer_already_found:
        errors.append(f"Body paragraph '{lines}' follows a footer")
    return False


def check_commit_msg(msg: str) -> List[str]:
    """
    Analyzes the commit message.

    Parameters
    ----------
    msg: str
        The commit message.

    Returns
    -------
    list of str:
        List of errors found.

    """
    errors = []
    paragraphs = msg.split("\n\n")
    header = paragraphs.pop(0)

    process_header(header, errors)
    footer_found = False
    for paragraph in paragraphs:
        found = process_paragraph(paragraph, footer_found, errors)
        footer_found = footer_found or found
    return errors


def conventional_commit_validator():
    """Entrypoint for the validator."""
    msg = get_commit_msg()
    errors = check_commit_msg(msg)
    if errors:
        print("Errors in commit message:")
        for error in errors:
            print(f"- {error}.")
        sys.exit(1)
    else:
        print("Commit message complies with conventional commits specification.")


if __name__ == "__main__":
    conventional_commit_validator()
