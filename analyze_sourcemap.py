import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\opencode_pro\build.js.map', 'r', encoding='utf-8') as f:
    data = json.load(f)

sources = data['sourcesContent']
names = data['sources']

# Search for BaseUrl, hardcoded URLs, API keys, secrets
patterns = {
    'BaseUrl': 'BaseUrl[^;]+',
    'turnstile': 'turnstile[^;]+',
    'sitekey': 'sitekey[^"\']+',
    'api_url': 'api[Uu]rl[^;]+',
    'base_url': 'base[Uu]rl[^;]+',
    'facetec': 'facetec[^;]+',
    'ondato_api': 'ondato[^;]*api[^;]+',
    'signalr': 'signalr[^;]+',
    'cloudflare': 'cloudflare[^;]+',
    'LicenseKey': 'LicenseKey[^;]+',
    'apiKey': 'apiKey[^;]+',
    'secret': 'secret[^;]+',
    'http_ondato': 'https?://[^;"\']*ondato[^;"\']*',
}

for label, pattern in patterns.items():
    print(f'\n=== {label} ===')
    for i, (name, content) in enumerate(zip(names, sources)):
        if content is None:
            continue
        for m in re.finditer(pattern, content, re.IGNORECASE):
            line_num = content[:m.start()].count('\n') + 1
            matched = m.group()[:200]
            print(f'  [{i}] {name}:L{line_num}: {matched}')

# Also find files that define BaseUrl
print('\n\n=== FILES REFERENCING BaseUrl ===')
for i, (name, content) in enumerate(zip(names, sources)):
    if content and 'BaseUrl' in content:
        first_line = content[:content.index('BaseUrl')]
        line_num = first_line.count('\n') + 1
        print(f'  [{i}] {name}:L{line_num}')
