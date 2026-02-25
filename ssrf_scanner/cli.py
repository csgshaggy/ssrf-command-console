import argparse
from ssrf_scanner.utils.logger import get_logger
from ssrf_scanner.utils.subnet import generate_ips_from_cidr
from ssrf_scanner.parallel_scan import scan_ips_parallel
from ssrf_scanner.exporters.json_exporter import export_results_to_json
from ssrf_scanner.dashboard_formatter import summarize_ip_result

logger = get_logger("cli")

def main():
    parser = argparse.ArgumentParser(description="Modular SSRF scanner")
    parser.add_argument("--cidr", help="CIDR to scan, e.g. 10.0.0.0/24")
    parser.add_argument("--ip", help="Single IP to scan")
    parser.add_argument("--output", help="Path to JSON output file", default=None)
    parser.add_argument("--workers", type=int, default=10, help="Max parallel workers")

    args = parser.parse_args()

    if not args.cidr and not args.ip:
        parser.error("You must provide either --cidr or --ip")

    if args.cidr:
        ips = generate_ips_from_cidr(args.cidr)
    else:
        ips = [args.ip]

    logger.info(f"Scanning {len(ips)} IP(s)...")

    results = scan_ips_parallel(ips, max_workers=args.workers)

    for ip, data in results.items():
        if "error" in data:
            logger.error(f"{ip}: error during scan: {data['error']}")
        else:
            summarize_ip_result(ip, data)

    if args.output:
        export_results_to_json(results, args.output)
        logger.info(f"Results written to {args.output}")


if __name__ == "__main__":
    main()
