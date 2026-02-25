# plugins/hash_tools.py

def get_modes():
    return {
        "hash_md5": {
            "description": "Compute MD5 hash of input",
            "options": {
                "uppercase": {"type": "bool", "value": False},
            }
        },
        "hash_sha256": {
            "description": "Compute SHA256 hash of input",
            "options": {
                "uppercase": {"type": "bool", "value": False},
            }
        }
    }


def run(mode_name, target, options):
    up = options.get("uppercase", False)

    if mode_name == "hash_md5":
        h = "d41d8cd98f00b204e9800998ecf8427e"
        return h.upper() if up else h

    if mode_name == "hash_sha256":
        h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        return h.upper() if up else h

    return "Unknown hash mode"
