"""Tests for clint.validator.Footer class."""
# pylint: disable=too-many-arguments
import pytest

from clint.validator import Footer, ValidatorException

from .conftest import INVALID_DATA, VALID_DATA


class TestFooterGenerate:
    """Tests for clint.validator.Footer.generate method."""

    @pytest.mark.parametrize("token", VALID_DATA["footer"]["tokens"])
    @pytest.mark.parametrize("separator", VALID_DATA["footer"]["separators"])
    def test_valid_generation(self, token, separator, sentence):
        """Test that all correct messages can generate a new footer object."""
        message = f"{token}{separator}{sentence}"
        footer = Footer.generate(msg=message)
        assert isinstance(footer, Footer)
        assert footer.token == token
        assert footer.separator == separator
        assert footer.description == sentence

    def test_empty_generation(self):
        """Test that empty message generation raises an exception."""
        with pytest.raises(ValidatorException):
            Footer.generate(msg="")


class TestFooterValidate:
    """Tests for clint.validator.Footer.validate method."""

    @pytest.mark.parametrize("token", VALID_DATA["footer"]["tokens"])
    @pytest.mark.parametrize("separator", VALID_DATA["footer"]["separators"])
    def test_valid_footer(self, token, separator, sentence, footer):
        """Test that all correct messages can generate a new footer object."""
        footer.token = token
        footer.separator = separator
        footer.description = sentence
        assert footer.validate()

    @pytest.mark.parametrize("token", INVALID_DATA["footer"]["tokens"])
    def test_invalid_token(self, token, sentence, footer):
        """Test that invalid token raises an exception."""
        footer.token = token
        footer.separator = VALID_DATA["footer"]["separators"][0]
        footer.description = sentence
        with pytest.raises(ValidatorException):
            footer.validate()

    @pytest.mark.parametrize("separator", INVALID_DATA["footer"]["separators"])
    def test_invalid_separator(self, separator, sentence, footer):
        """Test that invalid separator raises an exception."""
        footer.token = VALID_DATA["footer"]["tokens"][0]
        footer.separator = separator
        footer.description = sentence
        with pytest.raises(ValidatorException):
            footer.validate()

    @pytest.mark.parametrize("description", INVALID_DATA["footer"]["descriptions"])
    def test_invalid_description(self, description, footer):
        """Test that invalid separator raises an exception."""
        footer.token = VALID_DATA["footer"]["tokens"][0]
        footer.separator = VALID_DATA["footer"]["separators"][0]
        footer.description = description
        with pytest.raises(ValidatorException):
            footer.validate()
