import requests
import time
from typing import Optional, Dict, Any

def send_http_probe(url: str, timeout: float = 4.0) -> Dict[str, Any]:
    """
    Sends a synchronous HTTP GET request and returns structured metadata.
    """
    start = time.time()

    try:
        response = requests.get(url, timeout=timeout)
        elapsed = time.time() - start

        return {
            "url": url,
            "status": response.status_code,
            "headers": dict(response.headers),
            "content": response.text[:5000],  # safety cap
            "elapsed": elapsed,
            "error": None
        }

    except requests.exceptions.Timeout:
        return {
            "url": url,
            "status": None,
            "headers": {},
            "content": "",
            "elapsed": timeout,
            "error": "timeout"
        }

    except requests.exceptions.ConnectionError:
        return {
            "url": url,
            "status": None,
            "headers": {},
            "content": "",
            "elapsed": time.time() - start,
            "error": "connection_error"
        }

    except Exception as e:
        return {
            "url": url,
            "status": None,
            "headers": {},
            "content": "",
            "elapsed": time.time() - start,
            "error": str(e)
        }
