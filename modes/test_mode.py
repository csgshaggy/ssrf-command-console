MODE_NAME = "test_mode"


def run(target=None, options=None):
    return {
        "mode": MODE_NAME,
        "message": f"Test mode executed successfully. target={target!r}"
    }


def test_mode(target=None, options=None, state=None, dispatcher=None):
    try:
        result = run(target=target, options=options or {})
        return [
            "=== TEST MODE ===",
            result["message"],
            "=== END TEST MODE ==="
        ]
    except Exception as e:
        return [f"[test_mode ERROR] {e}"]
