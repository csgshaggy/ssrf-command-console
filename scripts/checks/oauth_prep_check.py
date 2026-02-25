# scripts/checks/oauth_prep_check.py

import os


def run():
    required_env = [
        "OAUTH_CLIENT_ID",
        "OAUTH_CLIENT_SECRET",
        "OAUTH_AUTH_URL",
        "OAUTH_TOKEN_URL",
        "OAUTH_REDIRECT_URI",
    ]

    missing = [k for k in required_env if not os.environ.get(k)]

    status = not missing
    details = "OK" if status else f"Missing env: {', '.join(missing)}"

    return {
        "name": "oauth_prep_check",
        "status": status,
        "details": details,
        "data": {"missing": missing},
    }
