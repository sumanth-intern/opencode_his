import requests, urllib3
urllib3.disable_warnings()

# Use IP directly with Host header
session = requests.Session()
session.headers.update({"Host": "www.parleagro.com"})

# Check brand/4 which gives 500
try:
    r = session.get("https://13.234.91.225/brand/4", timeout=10, verify=False)
    print(f"/brand/4 -> {r.status_code} ({len(r.content)}B)")
    print("Headers:", dict(r.headers))
    print("Body:")
    print(r.text[:2000])
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)[:100]}")

print("\n" + "="*60)

# Check the main page via IP
try:
    r = session.get("https://13.234.91.225/", timeout=10, verify=False)
    print(f"/ -> {r.status_code} ({len(r.content)}B)")
    # Look for interesting content
    if "Laravel" in r.text or "CSRF" in r.text:
        print("This is the Laravel site (www.parleagro.com)")
    elif "this   parleagro" in r.text:
        print("This is consumerconnect")
    else:
        print(f"First 200 chars: {r.text[:200]}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)[:100]}")

# Check login page via IP
try:
    r = session.get("https://13.234.91.225/login", timeout=10, verify=False)
    print(f"\n/login -> {r.status_code} ({len(r.content)}B)")
    print(r.text[:1000])
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)[:100]}")

# Check webmail 500 error content
print("\n" + "="*60)
print("\n=== WEBMAIL 500 ERRORS ===")
try:
    r = requests.get("https://webmail.parleagro.com/nonexistent", timeout=10, verify=False)
    print(f"/nonexistent -> {r.status_code} ({len(r.content)}B)")
    print(r.text[:1000])
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)[:100]}")
