import pytest

from registration import register_user, users


def test_register_valid_email():
    users.clear()
    result = register_user("user@example.com")
    assert result["status"] == "registered"
    assert "user@example.com" in users


def test_register_duplicate_email_raises_value_error():
    users.clear()
    register_user("user@example.com")
    with pytest.raises(ValueError, match=r"^User already registered$"):
        register_user("user@example.com")
    assert users == ["user@example.com"]


@pytest.mark.parametrize("email", ["", " ", "\t\n"])
def test_register_empty_or_whitespace_email_raises_value_error(email):
    users.clear()
    with pytest.raises(ValueError, match=r"^Email is required$"):
        register_user(email)
    assert users == []


@pytest.mark.parametrize(
    "email",
    [
        "not-an-email",  # missing '@' and domain dot
        "userexample.com",  # missing '@'
        "user@@example.com",  # multiple '@'
        "@example.com",  # empty local part
        "user@",  # empty domain
        "user@example",  # domain missing '.'
    ],
)
def test_register_invalid_email_raises_value_error(email):
    users.clear()
    with pytest.raises(ValueError, match=r"^Invalid email format$"):
        register_user(email)
    assert users == []
