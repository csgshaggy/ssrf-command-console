# plugins/text_tools.py

def get_modes():
    return {
        "text_upper": {
            "description": "Convert text to uppercase",
            "options": {}
        },
        "text_lower": {
            "description": "Convert text to lowercase",
            "options": {}
        }
    }


def run(mode_name, target, options):
    if mode_name == "text_upper":
        return target.upper()

    if mode_name == "text_lower":
        return target.lower()

    return "Unknown text mode"
