from typing import List
import ipaddress

def generate_ips_from_cidr(cidr: str) -> List[str]:
    """
    Given a CIDR like '10.0.0.0/24', return a list of IP strings.
    """
    network = ipaddress.ip_network(cidr, strict=False)
    return [str(ip) for ip in network.hosts()]
