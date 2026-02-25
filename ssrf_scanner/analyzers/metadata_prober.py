import requests


METADATA_ENDPOINTS = {
    "aws": "http://169.254.169.254/latest/meta-data/",
    "gcp": "http://169.254.169.254/computeMetadata/v1/",
    "azure": "http://169.254.169.254/metadata/instance",
}


def probe_metadata_endpoints(ip: str):
    """
    Very lightweight metadata probing placeholder.
    In a real SSRF, you'd route through the vulnerable server.
    Here we just return the endpoints we *would* try.
    """
    # For now, we don't actually call them (to avoid surprises).
    # We just describe what would be probed.
    results = []

    for provider, url in METADATA_ENDPOINTS.items():
        results.append({
            "provider": provider,
            "url": url,
            "note": "metadata endpoint candidate (requires SSRF path to be effective)",
        })

    return results
