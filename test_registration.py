import pytest

from registration import register_user, users


def test_register_valid_email():
    users.clear()
    result = register_user("user@example.com")
    assert result["status"] == "registered"
    assert "user@example.com" in users


def test_register_invalid_email_raises_value_error():
    users.clear()
    with pytest.raises(ValueError, match=r"^Invalid email format$"):
        register_user("not-an-email")
    assert users == []
