import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\opencode_pro\build.js.map', 'r', encoding='utf-8') as f:
    data = json.load(f)

sources = data['sourcesContent']
names = data['sources']

# Find FaceTec version and configuration
for i, (name, content) in enumerate(zip(names, sources)):
    if content is None:
        continue
    lower = content.lower()
    if 'facetec' not in lower and 'zoom' not in lower:
        continue

    for m in re.finditer(r'[^\n]{0,100}(?:FaceTecSDK|version[\'"]\s*:|FaceTec[A-Z]|v\d+\.\d+\.\d+)[^\n]{0,200}', content):
        snippet = m.group().strip()
        print(f'[{i}] {name.split("/")[-1]}: {snippet[:300]}')
        print()

# Also check the downloaded FaceTecSDK.js for version
print("\n=== FACE TEC SDK JS VERSION SCAN ===")
try:
    with open(r'F:\opencode_pro\facetec_sdk.js', 'r', encoding='utf-8') as f:
        content = f.read(500000)
    for m in re.finditer(r'(?:version|v\d+\.\d+\.\d+)[^\n]{0,100}', content[:100000], re.IGNORECASE):
        print(f'  {m.group()[:200]}')
except:
    print("  (not downloaded yet)")
