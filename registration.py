import re

users = []


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def register_user(email):
    if not isinstance(email, str) or not _EMAIL_RE.match(email):
        raise ValueError("Invalid email format")
    users.append(email)
    return {"status": "registered", "email": email}
