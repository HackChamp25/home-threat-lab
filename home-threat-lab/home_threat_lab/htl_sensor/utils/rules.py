import re

def suspecious_dns_length(dns_info, threshold=50):
    """Alert if DNS query is unusually long (Possible DGA)."""
    if dns_info and len(dns_info["query"]) > threshold:
        return{
            "type": "Suspecious DNS query length",
            "description": f"query {dns_info['query']} is unusually long ({len(dns_info)}) chars)",
            "recommendation": "check for possible DGA/malware communication",
            "severity": "High",
            "evidence": dns_info    
        }

def excessive_nxdomain(dns_info, rcode, failure_count, threshold=5):
    """Alert if too many NXDOMAIN failures in a short span."""
    if dns_info and rcode !=0 and failure_count >= threshold:
        return{
            "type": "NXDOMAIN Flood",
            "description": f"Device triggered {failure_count} failed DNS lookups",
            "recommendation": "Inspect system for beaconing/misconfiguration",
            "severity": "high",
            "evidence": dns_info
        }
    return None

def unusual_port(packet):
    """Alert if traffic is observed on uncommon port."""
    if hasattr(packet, "sport") and packet.sport not in (53,80,443):
        return{
            "type": "Unusual Port Usage",
            "description": f"Traffic on unusual port {packet.sport}",
            "recommendation": "Investigate whether this service is expected",
            "severity": "medium",
            "evidence": {"sport": packet.sport}
        }
    return None

def suspicious_evil_domain(dns_info):
    query = dns_info.get("query","")
    if dns_info["query"].endswith(".evil."):
        return{
            "type": "dns_suspicious",
            "description": f"Suspicious DNS query: {query}",
            "recommendation": "Block this domain and inspect the device.",
            "severity": "high",
            "evidence": dns_info,
        }


RULES = [suspecious_dns_length, excessive_nxdomain, unusual_port,suspicious_evil_domain]


