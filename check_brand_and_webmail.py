import requests, urllib3, re
urllib3.disable_warnings()

# Check brand endpoints
print("=== BRAND ENDPOINTS ===")
base = "https://www.parleagro.com"
for i in range(1, 20):
    try:
        r = requests.get(base + f"/brand/{i}", timeout=5, verify=False)
        if r.status_code != 404:
            print(f"/brand/{i} -> {r.status_code} ({len(r.content)}B) {r.text[:100]}")
    except:
        pass

# Try webmail via DNS
print("\n=== WEBMAIL (via DNS) ===")
try:
    r = requests.get("https://webmail.parleagro.com/", timeout=10, verify=False)
    print(f"Status: {r.status_code}")
    print(f"Server: {r.headers.get('Server', '?')}")
    # Find login form
    form = re.search(r'<form[^>]*>.*?</form>', r.text, re.DOTALL)
    if form:
        print("Form found:")
        print(form.group(0)[:1500])
    else:
        print("Body (first 2000 chars):")
        print(r.text[:2000])
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)[:100]}")

# Try to POST to webmail login
print("\n=== WEBMAIL LOGIN TEST ===")
try:
    r = requests.get("https://webmail.parleagro.com/", timeout=10, verify=False)
    html = r.text
    # Find form action
    action = re.search(r'<form[^>]+action=[\"\x27]([^\"\x27]+)[\"\x27]', html)
    if action:
        print(f"Form action: {action.group(1)}")
    # Find input names
    inputs = re.findall(r'<input[^>]+name=[\"\x27]([^\"\x27]+)[\"\x27]', html)
    print(f"Input names: {inputs}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)[:100]}")
