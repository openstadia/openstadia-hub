import secrets

SERVER_TOKEN_LENGTH = 16


def generate_server_token() -> str:
    return secrets.token_urlsafe(SERVER_TOKEN_LENGTH)
