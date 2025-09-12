import re

def extract_iocs(strings):
    """Extract basic IoCs (URLs, IPs, domains, hashes)."""
    urls = [s for s in strings if re.match(r"https?://", s)]
    ips = [s for s in strings if re.match(r"\b\d{1,3}(\.\d{1,3}){3}\b", s)]
    domains = [s for s in strings if re.match(r"\b[a-z0-9.-]+\.[a-z]{2,}\b", s)]
    hashes = [s for s in strings if re.match(r"\b[a-f0-9]{32,64}\b", s)]
    return {"urls": urls, "ips": ips, "domains": domains, "hashes": hashes}
