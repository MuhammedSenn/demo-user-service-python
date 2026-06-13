import pytest

from registration import get_user, get_user_count, register_user, unregister_user, users


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


def test_register_duplicate_email_is_case_insensitive():
    users.clear()
    register_user("User@Example.com")
    with pytest.raises(ValueError, match=r"^User already registered$"):
        register_user("user@example.com")
    assert users == ["user@example.com"]


def test_register_stores_normalized_email():
    users.clear()
    result = register_user("  User@Example.com  ")
    assert result["email"] == "user@example.com"
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


def test_get_user_count_returns_0_when_no_users_registered():
    users.clear()
    assert get_user_count() == 0


def test_get_user_count_returns_correct_count_after_registrations():
    users.clear()
    register_user("user1@example.com")
    assert get_user_count() == 1
    register_user("user2@example.com")
    assert get_user_count() == 2


def test_get_user_returns_normalized_email_case_insensitively_when_registered():
    users.clear()
    register_user("user@example.com")
    assert get_user("USER@Example.com") == "user@example.com"


def test_get_user_returns_none_when_not_registered():
    users.clear()
    register_user("user@example.com")
    assert get_user("other@example.com") is None


def test_unregister_user_removes_registered_email_case_insensitively_and_decrements_count():
    users.clear()
    register_user("user@example.com")
    assert get_user_count() == 1

    assert unregister_user("  USER@Example.com  ") is True
    assert get_user("user@example.com") is None
    assert get_user_count() == 0


def test_unregister_user_returns_false_when_email_not_registered():
    users.clear()
    register_user("user@example.com")
    assert unregister_user("other@example.com") is False
    assert users == ["user@example.com"]
