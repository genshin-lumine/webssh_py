import asyncssh

def build_key_auth(data):
    if "key_content" in data:
        key = asyncssh.import_private_key(data["key_content"])
        return {"client_keys": [key], "passphrase": data.get("passphrase")}
    else:
        return {"client_keys": [data["key_path"]], "passphrase": data.get("passphrase")}
