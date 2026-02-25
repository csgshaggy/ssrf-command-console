# plugins/utility_tools.py

def get_modes():
    return {
        "ping_host": {
            "description": "Ping a host (simulated)",
            "options": {
                "count": {"type": "int", "value": 4},
            }
        },
        "whois_lookup": {
            "description": "Perform a WHOIS lookup",
            "options": {
                "raw": {"type": "bool", "value": False},
            }
        }
    }


def run(mode_name, target, options):
    if mode_name == "ping_host":
        count = options.get("count", 4)
        return f"[ping_host] Pinging {target} {count} times (simulated)"

    if mode_name == "whois_lookup":
        raw = options.get("raw", False)
        return f"[whois_lookup] WHOIS for {target} (raw={raw}) (simulated)"

    return "Unknown utility mode"
