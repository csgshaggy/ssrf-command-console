import socket
import time

MODE_NAME = "dns_mode"


def run(target=None, options=None):
    if options is None:
        options = {}

    hostnames = options.get("hostnames", [
        "example.com",
        "metadata.google.internal",
        "169.254.169.254.nip.io",
        "internal.local",
        "test.ssrflab.com"
    ])

    timeout = options.get("timeout", 3)
    socket.setdefaulttimeout(timeout)

    results = []

    for host in hostnames:
        entry = {
            "hostname": host,
            "resolved": None,
            "error": None,
            "duration_ms": None
        }

        start = time.time()

        try:
            entry["resolved"] = socket.gethostbyname(host)
        except Exception as e:
            entry["error"] = str(e)
        finally:
            entry["duration_ms"] = round((time.time() - start) * 1000, 2)

        results.append(entry)

    return {
        "mode": MODE_NAME,
        "count": len(results),
        "results": results
    }


def dns_mode(target=None, options=None, state=None, dispatcher=None):
    try:
        result = run(target=target, options=options or {})
        lines = ["=== DNS MODE RESULTS ===", f"Total hostnames tested: {result['count']}", ""]

        for entry in result["results"]:
            host = entry["hostname"]
            resolved = entry["resolved"]
            error = entry["error"]
            duration = entry["duration_ms"]

            if resolved:
                lines.append(f"{host} → {resolved} ({duration} ms)")
            else:
                lines.append(f"{host} → ERROR: {error} ({duration} ms)")

        lines.append("")
        lines.append("=== END DNS MODE ===")
        return lines

    except Exception as e:
        return [f"[dns_mode ERROR] {e}"]
