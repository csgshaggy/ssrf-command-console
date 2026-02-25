def summarize_ip_result(ip_result: dict) -> dict:
    """
    Build a compact summary for dashboard display from a full scan result.
    """
    if "error" in ip_result:
        return {
            "ip": ip_result.get("ip"),
            "error": ip_result["error"],
        }

    return {
        "ip": ip_result.get("ip"),
        "anomaly_score": ip_result.get("anomaly_score", 0),
        "timing_anomalies": len(ip_result.get("timing_anomalies", [])),
        "clusters": {
            k: len(v) if isinstance(v, list) else v
            for k, v in ip_result.get("clusters", {}).items()
        },
        "patterns": ip_result.get("patterns", []),
        "redirects": ip_result.get("redirects", []),
        "banners": ip_result.get("banners", []),
        "fingerprints": ip_result.get("fingerprints", []),
        "metadata": ip_result.get("metadata", []),
        "header_mutations": ip_result.get("header_mutations", {}),
        "diffs": ip_result.get("diffs", []),
    }
