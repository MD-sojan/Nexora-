import re

def extract_iocs(strings):
    """Extract basic IoCs (URLs, IPs, domains, hashes)."""
    text = " ".join(strings)
    urls = re.findall(r"https?://[^\s]+", text)
    ips = re.findall(r"\b\d{1,3}(\.\d{1,3}){3}\b", text)
    domains = re.findall(r"\b[a-z0-9.-]+\.[a-z]{2,}\b", text)
    hashes = re.findall(r"\b[a-f0-9]{32,64}\b", text)
    return {"urls": list(set(urls)), "ips": list(set(ips)), "domains": list(set(domains)), "hashes": list(set(hashes))}
