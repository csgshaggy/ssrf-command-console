import concurrent.futures
from .scanner_core import scan_single_ip


def scan_ips_parallel(ips, max_workers=10):
    """
    Run SSRF scans across multiple IPs in parallel.
    Returns a dictionary:
    {
        "10.0.0.5": { ...result... },
        "10.0.0.6": { ...result... }
    }
    """
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {
            executor.submit(scan_single_ip, ip): ip for ip in ips
        }

        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                results[ip] = future.result()
            except Exception as e:
                results[ip] = {"error": str(e)}

    return results
