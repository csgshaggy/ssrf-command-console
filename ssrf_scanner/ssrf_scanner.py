from ssrf_scanner.paths import PATHS
from ssrf_scanner.ports import PORTS
from ssrf_scanner.scanner_core import probe_ip_across_ports_and_paths

from ssrf_scanner.analyzers.timing import detect_timing_anomalies
from ssrf_scanner.analyzers.size_cluster import cluster_by_response_size
from ssrf_scanner.analyzers.patterns import classify_error_patterns
from ssrf_scanner.analyzers.redirects import detect_redirects

from ssrf_scanner.utils.logger import get_logger

logger = get_logger("ssrf_scanner")


def scan_ip(ip: str):
    """
    High-level scan of a single IP across all ports and paths.
    Runs analyzers and prints results.
    """
    logger.info(f"Starting scan for IP: {ip}")

    results = probe_ip_across_ports_and_paths(ip, PORTS, PATHS)

    logger.info("Running analyzers...")

    timing = detect_timing_anomalies(results)
    clusters = cluster_by_response_size(results)
    patterns = classify_error_patterns(results)
    redirects = detect_redirects(results)

    return {
        "results": results,
        "timing_anomalies": timing,
        "clusters": clusters,
        "patterns": patterns,
        "redirects": redirects,
    }


def scan_subnet(ips: list):
    """
    Scan a list of IPs and return structured results.
    """
    all_results = {}

    for ip in ips:
        all_results[ip] = scan_ip(ip)

    return all_results
