import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\opencode_pro\facetec_sdk.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Extract version
version_matches = re.findall(r'(?:FaceTec\s+(?:SDK\s+)?(?:version|v)|"version"\s*:\s*"|Version\s*=|v)(\d+\.\d+[^"\';\s,)]*)', content)
print("=== FACE TEC SDK VERSIONS ===")
for v in set(version_matches):
    print(f"  Version: {v}")

# Extract FaceTecSDK version call
for m in re.finditer(r'version\s*\(\)\s*\{[^}]+return[^}]+}', content):
    print(f"  version() fn: {m.group()[:200]}")

# Search for config URLs, API keys, endpoints
print("\n=== CONFIG URLS / ENDPOINTS ===")
for m in re.finditer(r'(?:https?://[^"\';\s,)]+|api[^"\';\s]{4,30}|endpoint[^"\';\s]+)', content, re.IGNORECASE):
    url = m.group()[:150]
    if any(kw in url.lower() for kw in ['api', 'http', 'endpoint', 'server', 'url', 'face', 'ondato']):
        print(f"  {url}")

# Search for any hardcoded keys/secrets
print("\n=== SECRETS / KEYS ===")
for m in re.finditer(r'(?:key|secret|token|license)[^"\';\s]{0,20}["\':]\s*["\']([^"\';\s]{8,80})["\']', content, re.IGNORECASE):
    val = m.group(1)
    # Filter out common false positives
    if not any(fp in val.lower() for fp in ['key', 'token', 'true', 'false', 'null', 'undefined', 'string', 'number', 'function', 'object', 'length', 'prototype', 'return', 'this.']):
        if len(val) > 10:
            print(f"  {m.group()[:200]}")

# Check for CVE identifiers
print("\n=== CVE REFERENCES ===")
for m in re.finditer(r'CVE-\d{4}-\d{4,}', content, re.IGNORECASE):
    print(f"  {m.group()}")

# Check for debug mode
print("\n=== DEBUG / DEV MODE ===")
for m in re.finditer(r'(?:debug|development|isProduction|isDevelopment|enableLog)[^;]{0,100}', content):
    snippet = m.group()[:150]
    if any(kw in snippet.lower() for kw in ['true', 'false', '1', '0', 'yes', 'no']):
        print(f"  {snippet}")

# Count total size and license info
print(f"\n=== STATS ===")
print(f"  Total size: {len(content)} bytes")
print(f"  Lines: {content.count(chr(10))}")
# Check minification
if len(content) > 1000 and '{' in content[:100]:
    print(f"  First 200 chars: {content[:200]}")
