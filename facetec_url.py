import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\opencode_pro\facetec_sdk.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Try to extract/decode the string table
# FaceTec uses an array-based string encoding
# Find the string decoders
print("=== STRING DECODING FUNCTIONS ===")
for m in re.finditer(r'(function\s+\w+\s*\([\w,]+\).{0,500}(?:fromCharCode|charCodeAt|substring|slice)\s*\([^)]+\))', content):
    if m.group().count('{') < 5:  # simple decoder
        print(f"  {m.group()[:300]}\n")

# Look for FaceTec API endpoint
print("\n=== API ENDPOINT REFERENCES ===")
api_patterns = [
    r'FaceTecAPI[^;]{10,200}',
    r'api[Ff]ace[^;]{10,200}',
    r'[Ff]ace[Tt]ec[Aa]pi[^;]{10,200}',
    r'[Ff]ace[Tt]ec[Uu]rl[^;]{10,200}',
    r'[Aa]pi[Ee]ndpoint[^;]{10,200}',
    r'[Bb]ase[Uu]rl[^;]{10,200}',
    r'[Ff]ace[Tt]ec[^;]{0,50}(?:url|URL|Url|endpoint|Endpoint)[^;]{10,200}',
]
for pat in api_patterns:
    for m in re.finditer(pat, content):
        print(f"  {m.group()[:200]}")

# Look for the version string by finding FaceTec header/user-agent
print("\n=== USER AGENT / HEADERS ===")
for m in re.finditer(r'userAgentString.{0,200}', content, re.IGNORECASE):
    print(f"  {m.group()[:200]}")

for m in re.finditer(r'FaceTecAPIUserAgentString.{0,200}', content):
    print(f"  {m.group()[:200]}")

# Check for any version in plain text
print("\n=== PLAIN TEXT VERSIONS ===")
for m in re.finditer(r'\d+\.\d+\.\d+[^\s"\';\n,)]{,20}', content):
    v = m.group()
    if not v.startswith('3.293') and not any(p in v for p in ['0.0', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '1.1', '2.1']):
        print(f"  {v}")
