def fingerprint_services(probe_results):
    """
    Very simple heuristic fingerprinting based on headers and content.
    Returns a list of fingerprints per URL.
    """
    fingerprints = []

    for r in probe_results:
        data = r.to_dict()
        headers = data.get("headers", {}) or {}
        body_preview = (data.get("content_preview") or "")[:512].lower()

        fp = {
            "url": data.get("url"),
            "tags": [],
        }

        server = headers.get("Server", "").lower()

        if "nginx" in server:
            fp["tags"].append("nginx")
        if "apache" in server:
            fp["tags"].append("apache")
        if "iis" in server:
            fp["tags"].append("iis")
        if "tomcat" in server or "jetty" in body_preview:
            fp["tags"].append("java-app-server")
        if "wordpress" in body_preview:
            fp["tags"].append("wordpress")
        if "admin" in body_preview:
            fp["tags"].append("admin-panel")

        if fp["tags"]:
            fingerprints.append(fp)

    return fingerprints
