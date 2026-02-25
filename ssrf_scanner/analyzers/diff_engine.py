def diff_responses(probe_results):
    """
    Very simple diffing: group by status + content_length and note variations.
    """
    buckets = {}
    for r in probe_results:
        data = r.to_dict()
        key = (data.get("status"), data.get("content_length"))
        buckets.setdefault(key, []).append(data.get("url"))

    diffs = []
    for (status, size), urls in buckets.items():
        if len(urls) > 1:
            diffs.append({
                "status": status,
                "content_length": size,
                "urls": urls,
            })

    return diffs
