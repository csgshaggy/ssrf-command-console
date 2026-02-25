def extract_banners(probe_results):
    """
    Extract simple 'banners' from headers and content previews.
    Returns a list of dicts with url + banner info.
    """
    banners = []

    for r in probe_results:
        data = r.to_dict()
        headers = data.get("headers", {}) or {}
        server = headers.get("Server")
        powered_by = headers.get("X-Powered-By")
        title = data.get("title")  # if your ProbeResult tracks it

        if server or powered_by or title:
            banners.append({
                "url": data.get("url"),
                "server": server,
                "powered_by": powered_by,
                "title": title,
            })

    return banners
