import re

with open('F:\\opencode_pro\\_dev_docs.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.lower().find('oauth at fastmail')
if idx >= 0:
    section = text[idx:idx+25000]
    clean = re.sub(r'<script[^>]*>.*?</script>', '', section, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', '\n', clean)
    clean = re.sub(r'\n\s*\n', '\n\n', clean)
    print(clean.strip())
else:
    print('Section not found')
