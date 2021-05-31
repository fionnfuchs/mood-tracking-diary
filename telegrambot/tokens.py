import secrets


def create_secret_token():
    return secrets.token_urlsafe(16)