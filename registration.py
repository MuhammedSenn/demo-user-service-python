import re

users = []


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def register_user(email):
    if isinstance(email, str) and not email.strip():
        raise ValueError("Email is required")
    if not isinstance(email, str):
        raise ValueError("Invalid email format")

    normalized_email = email.strip().lower()

    if not _EMAIL_RE.match(normalized_email):
        raise ValueError("Invalid email format")

    users.append(normalized_email)
    return {"status": "registered", "email": normalized_email}
