import requests, json, hashlib, base64, secrets, sys

# Generate PKCE params
code_verifier = secrets.token_urlsafe(64)[:128]
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('ascii')).digest()).rstrip(b'=').decode()

client_id = '183e41ae'
state = secrets.token_urlsafe(16)

auth_url = ('https://api.fastmail.com/oauth/authorize'
    + '?client_id=' + client_id
    + '&redirect_uri=http://localhost/callback'
    + '&response_type=code'
    + '&scope=urn:ietf:params:jmap:core'
    + '&code_challenge_method=S256'
    + '&code_challenge=' + code_challenge
    + '&state=' + state)

print('=== PKCE PARAMS (save these) ===')
print('code_verifier: ' + code_verifier)
print('code_challenge: ' + code_challenge)
print('state: ' + state)
print('client_id: ' + client_id)
print()
print('=== AUTHORIZE URL (open this in your browser) ===')
print(auth_url)
print()
print('=== After logging in and authorizing ===')
print('You will be redirected to: http://localhost/callback?code=AUTH_CODE&state=' + state)
print('Share the full redirect URL (or just the code parameter) with me.')
