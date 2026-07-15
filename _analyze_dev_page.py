import re

with open('F:\\opencode_pro\\_dev_page.html', 'r', encoding='utf-8') as f:
    text = f.read()

links = re.findall(r'href=[\"\']([^\"\']+)[\"\']', text)
print('=== ALL LINKS ===')
for link in links:
    print(link)

title = re.search(r'<title>(.*?)</title>', text, re.IGNORECASE)
if title:
    print('\n=== TITLE ===')
    print(title.group(1))

for tag in ['h1', 'h2', 'h3']:
    headings = re.findall(r'<' + tag + r'[^>]*>(.*?)</' + tag + r'>', text, re.IGNORECASE)
    for h in headings:
        h2 = re.sub(r'<[^>]+>', '', h).strip()
        if h2:
            print(tag.upper() + ': ' + h2)

patterns = ['oauth', 'OAuth', 'client_id', 'redirect_uri', 'authorization', 'bearer', 'token', 'register']
for p in patterns:
    if p.lower() in text.lower():
        idx = text.lower().find(p.lower())
        start = max(0, idx - 100)
        end = min(len(text), idx + 200)
        snippet = text[start:end].replace('\n', ' ')
        print('\n=== Found "' + p + '" at ' + str(idx) + ' ===')
        print(snippet)
