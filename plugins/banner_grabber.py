# plugins/banner_grabber.py

def get_modes():
    return {
        "banner_grab": {
            "description": "Grab service banner from a host:port",
            "options": {
                "port": {"type": "int", "value": 80},
                "timeout": {"type": "int", "value": 3},
            }
        }
    }


def run(mode_name, target, options):
    if mode_name == "banner_grab":
        port = options.get("port", 80)
        return f"[banner_grab] Banner from {target}:{port} = <Simulated Banner>"

    return "Unknown banner grabber mode"
