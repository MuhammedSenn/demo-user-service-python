import re

users = []


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def register_user(email):
    if isinstance(email, str) and not email.strip():
        raise ValueError("Email is required")

    if isinstance(email, str):
        email = email.strip().lower()

    if not isinstance(email, str) or not _EMAIL_RE.match(email):
        raise ValueError("Invalid email format")
    if email in users:
        raise ValueError("User already registered")
    users.append(email)
    return {"status": "registered", "email": email}


def unregister_user(email):
    if isinstance(email, str):
        email = email.strip().lower()

    if not isinstance(email, str):
        return False

    try:
        users.remove(email)
    except ValueError:
        return False
    return True


def get_user(email):
    if isinstance(email, str):
        email = email.strip().lower()

    if not isinstance(email, str):
        return None

    return email if email in users else None


def get_user_count():
    return len(users)
