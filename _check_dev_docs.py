import requests, re
requests.packages.urllib3.disable_warnings()

r = requests.get('https://www.fastmail.com/dev/', timeout=15, verify=False, allow_redirects=True)
print('Status: ' + str(r.status_code) + ' (' + str(len(r.content)) + ' bytes)')

with open('F:\\opencode_pro\\_dev_docs.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

text = r.text
title = re.search(r'<title>(.*?)</title>', text, re.IGNORECASE)
if title:
    print('TITLE: ' + title.group(1))

for tag in ['h1', 'h2', 'h3']:
    headings = re.findall(r'<' + tag + r'[^>]*>(.*?)</' + tag + r'>', text, re.IGNORECASE)
    for h in headings:
        h2 = re.sub(r'<[^>]+>', '', h).strip()
        if h2:
            print(tag.upper() + ': ' + h2)

links = re.findall(r'href=[\"\']([^\"\']+)[\"\']', text)
print('\n=== INTERNAL LINKS ===')
for link in links:
    if link.startswith('/') and link != '/':
        print(link)
