import requests, json, sys
requests.packages.urllib3.disable_warnings()

hosts = ['www.fastmail.com', 'app.fastmail.com', 'betaapp.fastmail.com', 
         'api.fastmail.com', 'betaapi.fastmail.com', 'jmap.fastmail.com',
         'betajmap.fastmail.com', 'login.fastmail.com']

paths = [
    '/.well-known/oauth-authorization-server',
    '/.well-known/openid-configuration',
    '/oauth/register',
    '/oauth/authorize',
    '/oauth/token',
    '/oauth/refresh',
    '/oauth/registration',
    '/api/oauth/register',
    '/api/oauth/token',
    '/api/oauth/authorize',
    '/developer/',
    '/dev/',
    '/dev/oauth/',
]

for host in hosts:
    for path in paths:
        url = 'https://' + host + path
        try:
            r = requests.get(url, timeout=10, verify=False, allow_redirects=False)
            if r.status_code not in [404, 403, 405, 301, 302, 307, 308, 0]:
                print('[%d] %s%s' % (r.status_code, url, ' -> ' + r.headers.get('Location','') if r.status_code in [301,302,307,308] else ''))
        except Exception as e:
            pass

# Also check the developer docs for OAuth info
r = requests.get('https://www.fastmail.com/dev/', timeout=10, verify=False)
print('\n=== Dev docs page status: ' + str(r.status_code))
if r.status_code == 200:
    # Find OAuth-related links
    for line in r.text.split('\n'):
        if 'oauth' in line.lower():
            print('  OAUTH: ' + line.strip()[:200])
