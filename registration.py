import re

users = []


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def register_user(email):
    if isinstance(email, str) and not email.strip():
        raise ValueError("Email is required")
    if not isinstance(email, str) or not _EMAIL_RE.match(email):
        raise ValueError(
            "Invalid email format: must contain exactly one '@', a non-empty local part, and a domain containing a '.'"
        )
    users.append(email)
    return {"status": "registered", "email": email}
