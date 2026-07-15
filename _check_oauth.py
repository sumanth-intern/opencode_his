import requests, json
requests.packages.urllib3.disable_warnings()

urls = [
    'https://www.fastmail.com/.well-known/oauth-authorization-server',
    'https://app.fastmail.com/.well-known/oauth-authorization-server',
    'https://betaapp.fastmail.com/.well-known/oauth-authorization-server',
]
for url in urls:
    r = requests.get(url, verify=False)
    print('=== ' + url + ' ===')
    print('Status: ' + str(r.status_code))
    if r.status_code == 200:
        j = r.json()
        keys = ['registration_endpoint', 'token_endpoint', 'authorization_endpoint', 'token_endpoint_auth_methods_supported', 'code_challenge_methods_supported', 'grant_types_supported']
        for k in keys:
            print('  ' + k + ': ' + str(j.get(k, 'N/A')))
    print()
