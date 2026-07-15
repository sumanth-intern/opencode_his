import requests
import sys
import json
from datetime import datetime

TARGET = sys.argv[1] if len(sys.argv) > 1 else "https://paplweb.parleagro.com"
TARGET = TARGET.rstrip('/')

CHECKS = [
    # Source code / repo exposure
    ("/.git/config", 200, "Git config exposed"),
    ("/.git/HEAD", 200, "Git HEAD exposed"),
    ("/.gitignore", 200, ".gitignore exposed"),
    ("/.env", 200, "Environment file exposed"),
    ("/.env.bak", 200, "Environment backup exposed"),
    ("/.env.local", 200, "Local env exposed"),
    ("/.env.production", 200, "Production env exposed"),

    # Backup files
    ("/backup.zip", 200, "Backup archive"),
    ("/backup.tar.gz", 200, "Backup archive"),
    ("/backup.sql", 200, "Database backup"),
    ("/dump.sql", 200, "Database dump"),
    ("/db_backup.sql", 200, "Database backup"),
    ("/config.php.bak", 200, "Config backup"),
    ("/config.php.old", 200, "Config backup"),
    ("/config.php~", 200, "Config backup (vim)"),
    ("/config.php.swp", 200, "Config swap file"),

    # Documentation / info disclosure
    ("/server-info", 200, "Apache server-info"),
    ("/server-status", 200, "Apache server-status"),
    ("/docs/", 200, "Documentation directory"),
    ("/manual/", 200, "Apache manual"),
    ("/phpinfo.php", 200, "PHP info"),
    ("/info.php", 200, "PHP info"),
    ("/test.php", 200, "Test PHP file"),

    # Admin / management
    ("/admin/", 200, "Admin panel"),
    ("/administrator/", 200, "Administrator panel"),
    ("/cms/", 200, "CMS panel"),
    ("/backend/", 200, "Backend panel"),
    ("/panel/", 200, "Management panel"),
    ("/wp-admin/", 200, "WordPress admin"),
    ("/wp-content/", 200, "WordPress content"),

    # Common files with sensitive info
    ("/composer.json", 200, "Composer dependencies"),
    ("/composer.lock", 200, "Composer lock"),
    ("/package.json", 200, "NPM package info"),
    ("/robots.txt", [200, 403], "robots.txt"),
    ("/sitemap.xml", 200, "Sitemap"),
    ("/crossdomain.xml", 200, "Crossdomain policy"),
    ("/web.config", 200, "IIS web config"),

    # Directory listing
    ("/uploads/", [200, 403], "Uploads directory"),
    ("/assets/", [200, 403], "Assets directory"),
    ("/static/", [200, 403], "Static directory"),
    ("/img/", [200, 403], "Images directory"),
    ("/css/", [200, 403], "CSS directory"),
    ("/js/", [200, 403], "JS directory"),
]

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
})

findings = []
print(f"\n{'='*60}")
print(f"Exposed Files & Misconfig Scanner")
print(f"Target: {TARGET}")
print(f"{'='*60}\n")

for path, expected_status, description in CHECKS:
    if isinstance(expected_status, int):
        expected_status = [expected_status]
    url = f"{TARGET}{path}"
    try:
        r = session.get(url, timeout=10, allow_redirects=False)
        status = r.status_code
        if status in expected_status:
            size = len(r.content)
            snippet = ""
            if size > 0:
                content_type = r.headers.get('Content-Type', '')
                if 'text' in content_type or 'json' in content_type or size < 5000:
                    snippet = r.text[:300].strip()
            finding = {
                'url': url,
                'status': status,
                'size': size,
                'description': description,
                'snippet': snippet[:200] if snippet else "",
            }
            findings.append(finding)
            severity = "HIGH" if any(k in path for k in ['.git', '.env', 'backup', 'sql', 'info', 'server-', 'admin', 'administrator']) else "MEDIUM"
            print(f"  [{severity}] {status} {url}  ({size} bytes)")
            if snippet:
                print(f"          Content: {snippet[:150]}")
        elif status == 403:
            print(f"  [INFO ] 403 {url}  (exists but forbidden)")
    except Exception as e:
        print(f"  [ERROR] {url} - {e}")

print(f"\n{'='*60}")
print(f"Summary: {len(findings)} findings")
for f in findings:
    print(f"  [{f['status']}] {f['description']}: {f['url']} ({f['size']} bytes)")
print(f"{'='*60}")

with open('exposed_findings.json', 'w') as f:
    json.dump({'target': TARGET, 'findings': findings}, f, indent=2)
print("\n[*] Results saved to exposed_findings.json")
