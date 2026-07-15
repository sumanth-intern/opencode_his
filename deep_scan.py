import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\opencode_pro\build.js.map', 'r', encoding='utf-8') as f:
    data = json.load(f)

sources = data['sourcesContent']
names = data['sources']

patterns = [
    ('JWT Token', r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}'),
    ('Hex Key (32+ chars)', r'(?<!var )(?<!let )(?<!const )0x[a-fA-F0-9]{32,64}'),
    ('Base64 (40+ chars, likely secret)', r'[A-Za-z0-9+/]{40,}={0,2}'),
    ('API Key config', r'["\x27](?:api[Kk]ey|secret[Kk]ey|signing[Kk]ey|app[Kk]ey)["\x27]\s*[:=]\s*["\x27]([^"\x27]+)'),
    ('Turnstile/Sitekey', r'(?:turnstile|sitekey|captcha)[^;]{10,100}'),
    ('URL with credentials', r'https?://[^:@\s]+:[^:@\s]+@'),
]

for label, pattern in patterns:
    print(f'\n=== {label} ===')
    seen = set()
    count = 0
    for i, (name, content) in enumerate(zip(names, sources)):
        if content is None:
            continue
        for m in re.finditer(pattern, content, re.IGNORECASE):
            val = m.group()[:120]
            if val in seen:
                continue
            seen.add(val)
            line_num = content[:m.start()].count('\n') + 1
            count += 1
            if count <= 15:
                print(f'  [{i}] {name.split("/")[-1]}:L{line_num}: {val}')
    if count > 15:
        print(f'  ... and {count-15} more unique matches')
