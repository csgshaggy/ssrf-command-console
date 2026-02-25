# plugins/metadata_tools.py

def get_modes():
    return {
        "extract_meta": {
            "description": "Extract metadata from a URL",
            "options": {
                "include_headers": {"type": "bool", "value": True},
                "include_body": {"type": "bool", "value": False},
            }
        }
    }


def run(mode_name, target, options):
    if mode_name == "extract_meta":
        return f"[extract_meta] Metadata for {target}: <Simulated Metadata>"

    return "Unknown metadata mode"
