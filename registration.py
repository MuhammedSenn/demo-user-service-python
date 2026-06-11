users = []


def register_user(email):
    users.append(email)
    return {"status": "registered", "email": email}
