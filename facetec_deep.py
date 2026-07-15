import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\opencode_pro\facetec_sdk.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find the base API URL
print("=== PRODUCTION API URL ===")
for m in re.finditer(r'API_PROD_URL.{0,100}', content):
    print(f"  {m.group()[:150]}")

# Find FaceTec version patterns
print("\n=== VERSION PATTERNS ===")
for m in re.finditer(r'(?:version|FaceTec\s+SDK|v\d+\.\d+\.\d+|\d+\.\d+\.\d+)[^"]{0,200}', content, re.IGNORECASE):
    snippet = m.group()[:200]
    if any(c.isdigit() for c in snippet[:20]):
        print(f"  {snippet}")

# Find the FaceTecAPI URL  
print("\n=== API URLS ===")
for m in re.finditer(r'https?://[^"\';\s,)]+', content, re.IGNORECASE):
    url = m.group()[:200]
    print(f"  {url}")

# Check for FaceTec device SDK identifier
print("\n=== DEVICE SDK IDENTIFIER ===")
for m in re.finditer(r'(?:deviceSDK|DeviceSDK|sdkIdentifier|FaceTec_device)[^;]{0,150}', content, re.IGNORECASE):
    print(f"  {m.group()[:200]}")

# Find the license key pattern
print("\n=== LICENSE KEY ===")
for m in re.finditer(r'license[^;]{0,100}', content, re.IGNORECASE):
    print(f"  {m.group()[:200]}")
