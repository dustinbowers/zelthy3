import uuid


def default_config_key():
    return str(uuid.uuid4())[:6]
