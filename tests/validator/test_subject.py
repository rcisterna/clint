"""Tests for clint.validator.Subject class."""
# pylint: disable=too-many-arguments
import pytest

from clint.cli.result import Result
from clint.validator import Subject, ValidationException

from .conftest import INVALID_DATA, VALID_DATA


class TestSubjectGenerate:
    """Tests for clint.validator.Subject.generate method."""

    @pytest.mark.parametrize("c_type", VALID_DATA["subject"]["types"])
    @pytest.mark.parametrize("scope", VALID_DATA["subject"]["scopes"])
    @pytest.mark.parametrize("breaking", VALID_DATA["subject"]["breaking_changes"])
    @pytest.mark.parametrize("separator", VALID_DATA["subject"]["separators"])
    def test_valid_generation(self, c_type, scope, breaking, separator, sentence):
        """Test that all correct messages can generate a new subject object."""
        message = f"{c_type}{scope}{breaking}{separator}{sentence}"
        subject = Subject.generate(msg=message)
        assert isinstance(subject, Subject)
        assert subject.type == c_type
        assert subject.scope == scope
        assert subject.breaking == breaking
        assert subject.separator == separator
        assert subject.description == sentence

    def test_empty_generation(self):
        """Test that the minimum message can be generated."""
        subject = Subject.generate("")
        assert subject.type == ""
        assert subject.scope == ""
        assert subject.breaking == ""
        assert subject.separator == ""
        assert subject.description == ""


class TestSubjectValidate:
    """Tests for clint.validator.Subject.validate method."""

    @pytest.mark.parametrize("c_type", VALID_DATA["subject"]["types"])
    @pytest.mark.parametrize("scope", VALID_DATA["subject"]["scopes"])
    @pytest.mark.parametrize("breaking", VALID_DATA["subject"]["breaking_changes"])
    @pytest.mark.parametrize("separator", VALID_DATA["subject"]["separators"])
    def test_valid_subject(self, c_type, scope, breaking, separator, sentence, subject):
        """Test that all correct messages pass the validation."""
        subject.type = c_type
        subject.scope = scope
        subject.breaking = breaking
        subject.separator = separator
        subject.description = sentence
        result = Result(operation="test", base_error_code=0)
        subject.validate(result=result)
        assert result.return_code == 0

    @pytest.mark.parametrize("c_type", INVALID_DATA["subject"]["types"])
    def test_invalid_type(self, c_type, sentence, subject):
        """Test that invalid type raises an exception."""
        subject.type = c_type
        subject.separator = VALID_DATA["subject"]["separators"][0]
        subject.description = sentence
        result = Result(operation="test", base_error_code=0)
        subject.validate(result=result)
        assert result.return_code == 1

    @pytest.mark.parametrize("scope", INVALID_DATA["subject"]["scopes"])
    def test_invalid_scope(self, scope, sentence, subject):
        """Test that invalid scope raises an exception."""
        subject.type = VALID_DATA["subject"]["types"][0]
        subject.scope = scope
        subject.separator = VALID_DATA["subject"]["separators"][0]
        subject.description = sentence
        result = Result(operation="test", base_error_code=0)
        subject.validate(result=result)
        assert result.return_code == 1

    @pytest.mark.parametrize("separator", INVALID_DATA["subject"]["separators"])
    def test_invalid_separator(self, separator, sentence, subject):
        """Test that invalid separator raises an exception."""
        subject.type = VALID_DATA["subject"]["types"][0]
        subject.separator = separator
        subject.description = sentence
        result = Result(operation="test", base_error_code=0)
        subject.validate(result=result)
        assert result.return_code == 1

    @pytest.mark.parametrize("description", INVALID_DATA["subject"]["descriptions"])
    def test_invalid_description(self, description, subject):
        """Test that invalid description raises an exception."""
        subject.type = VALID_DATA["subject"]["types"][0]
        subject.separator = VALID_DATA["subject"]["separators"][0]
        subject.description = description
        result = Result(operation="test", base_error_code=0)
        subject.validate(result=result)
        assert result.return_code == 1
