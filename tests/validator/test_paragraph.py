"""Tests for clint.validator.Paragraph class."""
# pylint: disable=too-many-arguments
import pytest

from clint.validator import Paragraph, ValidatorException

from .conftest import INVALID_DATA, VALID_DATA


class TestParagraphGenerate:
    """Tests for clint.validator.Paragraph.generate method."""

    @pytest.mark.parametrize("text", VALID_DATA["body"]["texts"])
    def test_valid_generation(self, text):
        """Test that all correct messages can generate a new object."""
        paragraph = Paragraph.generate(msg=text)
        assert isinstance(paragraph, Paragraph)
        assert paragraph.text == text
        assert paragraph.is_pure

    def test_empty_generation(self):
        """Test that the minimum message can be generated."""
        paragraph = Paragraph.generate(msg="")
        assert paragraph.text == ""
        assert paragraph.is_pure
        assert len(paragraph.footers) == 0


class TestParagraphValidate:
    """Tests for clint.validator.Paragraph.validate method."""

    @pytest.mark.parametrize("text", VALID_DATA["body"]["texts"])
    def test_valid_paragraph(self, text, paragraph):
        """Test that all correct messages can generate a new paragraph object."""
        paragraph.text = text
        assert paragraph.validate()

    @pytest.mark.parametrize("text", INVALID_DATA["body"]["texts"])
    def test_invalid_text(self, text, paragraph):
        """Test that invalid text raises an exception."""
        paragraph.text = text
        with pytest.raises(ValidatorException):
            paragraph.validate()
