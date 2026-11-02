# Nmap XML Inventory Parsing

Nmap XML is a structured export format. This chapter focuses on parsing an existing report from an authorized inventory scan, not selecting targets or automating scans.

```python
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_inventory(path: Path) -> list[dict]:
    root = ET.parse(path).getroot()
    hosts = []
    for host in root.findall("host"):
        address = host.find("address")
        status = host.find("status")
        hosts.append({
            "address": address.get("addr") if address is not None else None,
            "state": status.get("state") if status is not None else "unknown",
        })
    return hosts
```

Treat imported XML as untrusted input. For files from untrusted sources, consider hardened XML parsing and enforce file-size limits.
