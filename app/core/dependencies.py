"""
Core dependency functions for the SSRF Command Console backend.
These are lightweight, stateless helpers used by routers.
"""

from fastapi import Depends, Request
from app.core.config import settings


def get_settings():
    """
    Provide application settings as a dependency.
    Useful for routers or services that need config values.
    """
    return settings


def get_client_ip(request: Request) -> str:
    """
    Extract the client IP from the incoming request.
    Works with or without reverse proxies.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host
