# plugins/http_extra.py

def get_modes():
    return {
        "http_title_grab": {
            "description": "Fetch the <title> of a webpage",
            "options": {
                "timeout": {"type": "int", "value": 5},
            }
        },
        "http_header_dump": {
            "description": "Dump HTTP response headers",
            "options": {
                "timeout": {"type": "int", "value": 5},
                "follow_redirects": {"type": "bool", "value": True},
            }
        }
    }


def run(mode_name, target, options):
    if mode_name == "http_title_grab":
        return f"[http_title_grab] Title for {target}: <Simulated Title>"

    if mode_name == "http_header_dump":
        return f"[http_header_dump] Headers for {target}: <Simulated Headers>"

    return "Unknown HTTP plugin mode"
