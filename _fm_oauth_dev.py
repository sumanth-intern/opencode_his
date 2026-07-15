import requests, re, sys
requests.packages.urllib3.disable_warnings()

# Check developer docs for OAuth
r = requests.get('https://www.fastmail.com/developer/', timeout=15, verify=False, allow_redirects=True)
print('Status: ' + str(r.status_code) + ' (' + str(len(r.content)) + ' bytes)')
text = r.text

# Save the page to search manually
with open('F:\\opencode_pro\\_dev_page.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Find all links
links = re.findall(r'href=["\']([^"\']+)["\']', text, re.IGNORECASE)
oauth_links = []
for link in links:
    if 'oauth' in link.lower() or 'token' in link.lower() or 'authorize' in link.lower():
        oauth_links.append(link)

print('OAuth/token/authorize links found:')
for link in oauth_links[:20]:
    print('  ' + link)

# Find OAuth-related text blocks
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'oauth' in line.lower():
        print('Line ' + str(i) + ': ' + line.strip()[:300])
