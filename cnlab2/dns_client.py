#!/usr/bin/env python3
import logging
import socket
from datetime import datetime
try:
    import dns.resolver
except Exception:
    dns = None

logging.basicConfig(filename="dns_client.log", level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

domain = input("Enter domain to query (press Enter for example.com): ").strip() or "example.com"
print(f"→ Resolving DNS records for {domain} (this may take a second)...")

def resolve_a(domain):
    results = []
    if dns:
        try:
            ans = dns.resolver.resolve(domain, "A")
            for r in ans:
                results.append(str(r))
        except Exception:
            pass
    try:
        names = socket.gethostbyname_ex(domain)[2]
        for ip in names:
            if ip not in results:
                results.append(ip)
    except Exception:
        pass
    return results

def resolve_mx(domain):
    results = []
    if not dns:
        return results
    try:
        ans = dns.resolver.resolve(domain, "MX")
        for r in ans:
            results.append(f"{r.preference} {r.exchange.to_text()}")
    except Exception:
        pass
    return results

def resolve_cname(domain):
    results = []
    if not dns:
        return results
    try:
        ans = dns.resolver.resolve(domain, "CNAME")
        for r in ans:
            results.append(r.target.to_text())
    except Exception:
        pass
    return results

a = resolve_a(domain)
mx = resolve_mx(domain)
cname = resolve_cname(domain)

lines = []
lines.append(f"DNS Query results for {domain} at {datetime.utcnow().isoformat()} UTC")
lines.append("A records:")
lines.extend("  " + r for r in (a or ["(none)"]))
lines.append("MX records:")
lines.extend("  " + r for r in (mx or ["(none)"]))
lines.append("CNAME records:")
lines.extend("  " + r for r in (cname or ["(none)"]))

out = "\n".join(lines)
print("\n" + out)
with open("dns_results.txt", "w", encoding="utf-8") as f:
    f.write(out)
logging.info("Wrote dns_results.txt for %s", domain)
print("\n✅ Results saved to dns_results.txt and dns_client.log")