"""Tests for clint.validator.Commit class."""
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
from unittest.mock import MagicMock

import pytest

from clint.validator import Commit, Paragraph, Subject, ValidationException

from .conftest import faker, COMMITS_INFO


class TestCommitGetParagraphs:
    """Tests for clint.validator.Commit.get_paragraphs method."""

    @pytest.mark.parametrize("commit_info", COMMITS_INFO)
    def test_valid_generation(self, commit_info):
        """Test that all correct messages can generate a new commit object."""
        paragraphs = Commit.get_paragraphs(msg=commit_info["msg"])
        assert len(paragraphs) == commit_info["paragraphs"]
        if paragraphs:
            assert not paragraphs[-1].endswith("\n")


class TestCommitGenerate:
    """Tests for clint.validator.Commit.generate method."""

    @pytest.mark.parametrize("commit_info", COMMITS_INFO)
    def test_valid_generation(self, commit_info):
        """Test that all correct messages can generate a new commit object."""
        commit = Commit.generate(msg=commit_info["msg"])
        assert isinstance(commit, Commit)
        assert isinstance(commit.subject, Subject)
        paragraphs = (
            commit_info["paragraphs"] - 1 if commit_info["paragraphs"] > 0 else 0
        )
        assert len(commit.paragraphs) == paragraphs
        for paragraph in commit.paragraphs:
            assert isinstance(paragraph, Paragraph)


@pytest.mark.usefixtures("mock_subject_validate", "mock_paragraph_validate")
class TestCommitValidate:
    """Tests for clint.validator.Commit.validate method."""

    # pylint: disable=unused-argument

    mock_subject_validate = MagicMock
    mock_paragraph_validate = MagicMock

    def test_valid_attributes(self, commit, paragraph, mock_clean_validations):
        """Test validation if all attribute validation passes."""
        commit.paragraphs = (paragraph,)
        assert commit.validate()
        commit.subject.validate.assert_called_once()
        paragraph.validate.assert_called_once()

    def test_invalid_subject(self, commit, paragraph, mock_clean_validations):
        """Test validation if subject validation fails."""
        self.mock_subject_validate.side_effect = ValidationException
        commit.paragraphs = (paragraph,)
        with pytest.raises(ValidationException):
            assert commit.validate()
        commit.subject.validate.assert_called_once()
        paragraph.validate.assert_not_called()

    def test_invalid_paragraph(self, commit, paragraph, mock_clean_validations):
        """Test validation if subject validation fails."""
        self.mock_paragraph_validate.side_effect = ValidationException
        commit.paragraphs = (paragraph,)
        with pytest.raises(ValidationException):
            assert commit.validate()
        commit.subject.validate.assert_called_once()
        paragraph.validate.assert_called_once()
