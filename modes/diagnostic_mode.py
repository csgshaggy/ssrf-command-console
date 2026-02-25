MODE_NAME = "diagnostic_mode"


def run(state=None, dispatcher=None):
    return {
        "mode": MODE_NAME,
        "loaded_modes": list(dispatcher.modes.keys()) if dispatcher else [],
        "state_ok": state is not None
    }


def diagnostic_mode(state=None, dispatcher=None):
    try:
        result = run(state=state, dispatcher=dispatcher)

        lines = [
            "=== DIAGNOSTIC MODE ===",
            f"State attached: {result['state_ok']}",
            "",
            "Loaded modes:"
        ]

        for m in result["loaded_modes"]:
            lines.append(f" - {m}")

        lines.append("")
        lines.append("=== END DIAGNOSTIC MODE ===")
        return lines

    except Exception as e:
        return [f"[diagnostic_mode ERROR] {e}"]
