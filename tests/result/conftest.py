"""Configuration for result tests."""
import pytest

from clint.result import Result


def get_result() -> Result:
    """Get Result instance without actions."""
    return Result(operation="test", base_error_code=0)


@pytest.fixture(name="result_empty")
def fixture_result_empty() -> Result:
    """Fixture to get a Result instance without actions."""
    return get_result()


@pytest.fixture
def result_with_non_error_action(result_empty, sentence) -> Result:
    """Fixture to get a Result instance with non error action."""
    return result_empty.add_action(action="no_error", message=sentence, is_error=False)


@pytest.fixture
def result_with_error_action(result_empty, sentence) -> Result:
    """Fixture to get a Result instance with non error action."""
    return result_empty.add_action(action="error", message=sentence, is_error=True)
