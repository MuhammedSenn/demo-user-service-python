from registration import register_user, users


def test_register_valid_email():
    users.clear()
    result = register_user("user@example.com")
    assert result["status"] == "registered"
    assert "user@example.com" in users
