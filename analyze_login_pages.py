import requests, urllib3, re
urllib3.disable_warnings()

# Webmail analysis
r = requests.get('https://webmail.parleagro.com/index.php', timeout=10, verify=False)
form_match = re.search(r'<form[^>]*action=[\"\x27]([^\"\x27]+)[\"\x27].*?</form>', r.text, re.DOTALL)
print("=== WEBMAIL ===")
if form_match:
    print("LOGIN FORM:")
    print(form_match.group(0)[:2000])
else:
    print("First 3000 chars:")
    print(r.text[:3000])

# Find meta tags with enckey, encval
meta_keys = re.findall(r'<meta[^>]+>', r.text)
for m in meta_keys:
    if 'enc' in m.lower():
        print("META:", m)

# Laravel login analysis
r2 = requests.get('https://www.parleagro.com/login', timeout=10, verify=False)
form_match2 = re.search(r'<form[^>]*action=[\"\x27]([^\"\x27]+)[\"\x27].*?</form>', r2.text, re.DOTALL)
print("\n=== LARAVEL LOGIN ===")
if form_match2:
    print("LOGIN FORM:")
    print(form_match2.group(0)[:2000])
else:
    print("First 2000 chars:")
    print(r2.text[:2000])

# Find CSRF meta
csrf = re.findall(r'<meta[^>]*csrf[^>]+>', r2.text, re.IGNORECASE)
for c in csrf:
    print("CSRF META:", c)
