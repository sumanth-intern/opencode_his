import requests, re
requests.packages.urllib3.disable_warnings()

urls = [
    'https://www.fastmail.com/dev/',
    'https://www.fastmail.com/developer/',
    'https://www.fastmail.com/developers/',
    'https://www.fastmail.com/api/',
    'https://www.fastmail.com/documentation/',
]
for url in urls:
    try:
        r = requests.get(url, timeout=15, verify=False, allow_redirects=True)
        print(url + ' => ' + str(r.status_code) + ' (' + str(len(r.content)) + ' bytes)')
        links = re.findall(r'href=["\'](.*?oauth.*?)["\']', r.text, re.IGNORECASE)
        if links:
            print('  OAuth links: ' + str(links[:5]))
        if 'oauth' in r.text.lower():
            print('  Contains OAuth text')
    except Exception as e:
        print(url + ' => ERROR: ' + str(e))
