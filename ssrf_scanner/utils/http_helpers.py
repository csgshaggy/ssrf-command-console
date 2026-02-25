def send_http_probe(url, timeout=3):
    """
    Sends a simple HTTP GET request to the target URL.
    Always returns a dictionary containing:
    - url
    - status_code
    - content_length
    - headers
    - redirects
    - error
    """
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)

        return {
            "url": url,
            "status_code": response.status_code,
            "content_length": len(response.content),
            "headers": dict(response.headers),
            "redirects": [r.url for r in response.history],
            "error": None
        }

    except Exception as e:
        return {
            "url": url,
            "status_code": None,
            "content_length": None,
            "headers": {},
            "redirects": [],
            "error": str(e)
        }
