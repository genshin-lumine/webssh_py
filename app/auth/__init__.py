from .password import build_password_auth
from .key import build_key_auth


def build_auth_params(data):
    auth_type = data["auth_type"]

    if auth_type == "password":
        return build_password_auth(data)
    elif auth_type == "key":
        return build_key_auth(data)
    else:
        raise ValueError(f"不支持的认证方式: {auth_type}")
