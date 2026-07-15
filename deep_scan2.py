import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\opencode_pro\build.js.map', 'r', encoding='utf-8') as f:
    data = json.load(f)

sources = data['sourcesContent']
names = data['sources']

patterns = [
    # Hardcoded API keys/secrets (key: value pattern)
    ('API Key/Secret', r'["\x27](?:apiKey|secretKey|signingKey|appKey|privateKey)["\x27]\s*[:=]\s*["\x27]([^"\x27]{8,80})["\x27]'),
    # Turnstile/captcha keys
    ('Turnstile Key', r'(?:turnstile|sitekey)[^;=]{0,20}[:=]\s*["\x27]?([a-zA-Z0-9_-]{20,60})'),
    # FaceTec license keys  
    ('FaceTec Key', r'(?:deviceKeyIdentifier|publicFaceScanEncryptionKey)[^;]{10,100}'),
    # Stripe/API keys pattern
    ('Stripe/API Key', r'(?:sk_live_|pk_live_|sk_test_|pk_test_|rk_live_|rk_test_)[a-zA-Z0-9]+'),
    # AWS keys
    ('AWS Key', r'(?:AKIA[0-9A-Z]{16})'),
    # Twilio
    ('Twilio Key', r'(?:AC[a-f0-9]{32}|SK[a-f0-9]{32})'),
    # Private keys
    ('Private Key', r'-----BEGIN\s+(?:RSA|EC|DSA|PRIVATE)\s+KEY-----'),
    # URLs with embedded credentials
    ('Credential URL', r'https?://[^:@/\s]+:[^:@/\s]+@[^\s"\x27]{5,100}'),
    # Exposed tokens in config
    ('Token Config', r'["\x27](?:token|accessToken|refreshToken|apiToken)["\x27]\s*[:=]\s*["\x27]([^"\x27]{20,200})["\x27]'),
]

for label, pattern in patterns:
    print(f'\n=== {label} ===')
    seen = set()
    count = 0
    for i, (name, content) in enumerate(zip(names, sources)):
        if content is None:
            continue
        for m in re.finditer(pattern, content, re.IGNORECASE):
            val = m.group()[:150]
            if val in seen:
                continue
            seen.add(val)
            line_num = content[:m.start()].count('\n') + 1
            count += 1
            short_name = name.split('/')[-1]
            if count <= 15:
                print(f'  [{i}] {short_name}:L{line_num}: {val}')
    if count > 15:
        print(f'  ... and {count-15} more unique matches')
