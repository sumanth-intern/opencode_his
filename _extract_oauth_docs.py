import re

with open('F:\\opencode_pro\\_dev_docs.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find OAuth section
idx = text.lower().find('oauth at fastmail')
if idx >= 0:
    start = max(0, idx - 500)
    section = text[start:idx+15000]
    # Clean up HTML tags for readability
    clean = re.sub(r'<script[^>]*>.*?</script>', '', section, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', '\n', clean)
    clean = re.sub(r'\n\s*\n', '\n\n', clean)
    print('=== OAuth SECTION ===')
    print(clean.strip()[:5000])
else:
    print('OAuth at Fastmail section not found')
