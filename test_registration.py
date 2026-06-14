import pytest

from registration import (
    get_user,
    get_user_count,
    list_users,
    register_user,
    register_users,
    unregister_user,
    update_user_email,
    users,
)


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


def test_register_email_too_long_raises_value_error():
    users.clear()
    # Ensure normalized email length is 255 (> 254) while still matching the simple format regex.
    email = "a" * 243 + "@example.com"  # 243 + 12 = 255
    assert len(email) == 255
    with pytest.raises(ValueError, match=r"^Email is too long$"):
        register_user(email)
    assert users == []


def test_register_normal_length_email_still_registers_successfully():
    users.clear()
    email = "a" * 242 + "@example.com"  # 242 + 12 = 254
    assert len(email) == 254
    result = register_user(email)
    assert result["status"] == "registered"
    assert result["email"] == email
    assert users == [email]


def test_register_users_returns_per_email_report_and_does_not_abort_on_errors():
    users.clear()
    register_user("taken@example.com")

    report = register_users(
        [
            "new@example.com",
            "not-an-email",
            "taken@example.com",
            "  Another@Example.com  ",
        ]
    )

    assert report == {
        "results": [
            {"status": "registered", "email": "new@example.com"},
            {"status": "error", "email": "not-an-email", "error": "Invalid email format"},
            {
                "status": "error",
                "email": "taken@example.com",
                "error": "User already registered",
            },
            {"status": "registered", "email": "another@example.com"},
        ]
    }

    assert sorted(users) == sorted(["taken@example.com", "new@example.com", "another@example.com"])


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


def test_unregister_registered_user_removes_user_and_returns_status():
    users.clear()
    register_user("user@example.com")
    assert get_user_count() == 1

    result = unregister_user("user@example.com")
    assert result == {"status": "unregistered", "email": "user@example.com"}
    assert get_user("user@example.com") is None
    assert get_user_count() == 0
    assert users == []


def test_unregister_is_case_insensitive_and_normalizes_email():
    users.clear()
    register_user("user@example.com")

    result = unregister_user("USER@Example.com")
    assert result == {"status": "unregistered", "email": "user@example.com"}
    assert users == []


def test_unregister_nonexistent_user_raises_and_leaves_users_unchanged():
    users.clear()
    register_user("user@example.com")
    before = list(users)

    with pytest.raises(ValueError, match=r"^User not found$"):
        unregister_user("other@example.com")

    assert users == before
    assert get_user_count() == 1


@pytest.mark.parametrize("email", ["", " ", "\t\n"])
def test_unregister_empty_or_whitespace_email_raises_value_error(email):
    users.clear()
    register_user("user@example.com")
    before = list(users)

    with pytest.raises(ValueError, match=r"^Email is required$"):
        unregister_user(email)

    assert users == before


def test_update_user_email_successful_update():
    users.clear()
    register_user("old@example.com")

    result = update_user_email("old@example.com", "new@example.com")
    assert result == {
        "status": "updated",
        "old_email": "old@example.com",
        "email": "new@example.com",
    }
    assert users == ["new@example.com"]


def test_update_user_email_nonexistent_user_raises_and_leaves_users_unchanged():
    users.clear()
    register_user("user@example.com")
    before = list(users)

    with pytest.raises(ValueError, match=r"^User not found$"):
        update_user_email("missing@example.com", "new@example.com")

    assert users == before


@pytest.mark.parametrize("new_email", ["", " ", "\t\n", "not-an-email"])
def test_update_user_email_invalid_new_email_raises_and_leaves_users_unchanged(new_email):
    users.clear()
    register_user("old@example.com")
    before = list(users)

    expected = (
        r"^Email is required$"
        if isinstance(new_email, str) and not new_email.strip()
        else r"^Invalid email format$"
    )
    with pytest.raises(ValueError, match=expected):
        update_user_email("old@example.com", new_email)

    assert users == before


def test_update_user_email_new_email_collision_raises_and_leaves_users_unchanged():
    users.clear()
    register_user("old@example.com")
    register_user("taken@example.com")
    before = list(users)

    with pytest.raises(ValueError, match=r"^User already registered$"):
        update_user_email("old@example.com", "taken@example.com")

    assert users == before


def test_update_user_email_case_only_no_op_returns_success_and_leaves_users_unchanged():
    users.clear()
    register_user("user@example.com")
    before = list(users)

    result = update_user_email("USER@Example.com", "  User@Example.com  ")
    assert result == {
        "status": "updated",
        "old_email": "user@example.com",
        "email": "user@example.com",
    }
    assert users == before


def test_list_users_returns_empty_list_when_no_users_registered():
    users.clear()
    assert list_users() == []


def test_list_users_returns_sorted_copy_of_registered_emails():
    users.clear()
    register_user("b@example.com")
    register_user("a@example.com")

    listed = list_users()
    assert listed == ["a@example.com", "b@example.com"]

    # Ensure it's a copy and not the internal list
    listed.append("c@example.com")
    assert users == ["b@example.com", "a@example.com"]
