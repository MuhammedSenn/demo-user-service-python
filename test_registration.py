import pytest

from registration import register_user, users


def test_register_valid_email():
    users.clear()
    result = register_user("user@example.com")
    assert result["status"] == "registered"
    assert "user@example.com" in users


def test_register_email_is_normalized_stripped_and_lowercased():
    users.clear()
    result = register_user("  UsEr@Example.COM \t\n")
    assert result["status"] == "registered"
    assert result["email"] == "user@example.com"
    assert users == ["user@example.com"]


@pytest.mark.parametrize("email", ["", " ", "\t\n"])
def test_register_empty_or_whitespace_email_raises_value_error(email):
    users.clear()
    with pytest.raises(ValueError, match=r"^Email is required$"):
        register_user(email)
    assert users == []


def test_register_invalid_email_raises_value_error():
    users.clear()
    with pytest.raises(ValueError, match=r"^Invalid email format$"):
        register_user("not-an-email")
    assert users == []
