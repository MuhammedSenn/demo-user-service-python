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

    if len(email) > 254:
        raise ValueError("Email is too long")

    if email in users:
        raise ValueError("User already registered")
    users.append(email)
    return {"status": "registered", "email": email}


def update_user_email(old_email, new_email):
    if isinstance(old_email, str):
        old_email = old_email.strip().lower()

    if not isinstance(old_email, str):
        raise ValueError("User not found")

    if old_email not in users:
        raise ValueError("User not found")

    if isinstance(new_email, str) and not new_email.strip():
        raise ValueError("Email is required")

    if isinstance(new_email, str):
        new_email = new_email.strip().lower()

    if not isinstance(new_email, str) or not _EMAIL_RE.match(new_email):
        raise ValueError("Invalid email format")

    if len(new_email) > 254:
        raise ValueError("Email is too long")

    if new_email == old_email:
        return {"status": "updated", "old_email": old_email, "email": new_email}

    if new_email in users:
        raise ValueError("User already registered")

    idx = users.index(old_email)
    users[idx] = new_email
    return {"status": "updated", "old_email": old_email, "email": new_email}


def unregister_user(email):
    if isinstance(email, str) and not email.strip():
        raise ValueError("Email is required")

    if isinstance(email, str):
        email = email.strip().lower()

    if not isinstance(email, str):
        raise ValueError("User not found")

    try:
        users.remove(email)
    except ValueError as exc:
        raise ValueError("User not found") from exc

    return {"status": "unregistered", "email": email}


def get_user(email):
    if isinstance(email, str):
        email = email.strip().lower()

    if not isinstance(email, str):
        return None

    return email if email in users else None


def get_user_count():
    return len(users)
