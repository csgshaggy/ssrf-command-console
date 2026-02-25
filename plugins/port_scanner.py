# plugins/port_scanner.py

def get_modes():
    return {
        "port_scan": {
            "description": "Scan common ports on a host",
            "options": {
                "ports": {"type": "str", "value": "22,80,443"},
                "timeout": {"type": "int", "value": 2},
            }
        }
    }


def run(mode_name, target, options):
    if mode_name == "port_scan":
        ports = options.get("ports", "22,80,443")
        return f"[port_scan] Scanned {target} on ports {ports} (simulated)"

    return "Unknown port scanner mode"
