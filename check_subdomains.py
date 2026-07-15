import requests, urllib3, socket
urllib3.disable_warnings()

targets = [
    'https://www.parleagro.com',
    'http://www.parleagro.com',
    'https://webmail.parleagro.com',
    'http://webmail.parleagro.com',
    'https://intranet.parleagro.com',
    'http://intranet.parleagro.com',
    'https://analytics.parleagro.com',
    'http://analytics.parleagro.com',
    'https://smtp.parleagro.com',
    'https://imap.parleagro.com',
    'https://pop3.parleagro.com',
]

for u in targets:
    try:
        r = requests.get(u, timeout=5, verify=False, allow_redirects=False)
        srv = r.headers.get("Server", "?")
        ct = r.headers.get("Content-Type", "?")
        loc = r.headers.get("Location", "")
        print(f"{u} -> {r.status_code} [{srv}] [{len(r.content)}B] {ct}")
        if loc:
            print(f"  Location: {loc}")
        if len(r.text) < 200:
            print(f"  Body: {r.text[:200]}")
    except Exception as e:
        print(f"{u} -> {type(e).__name__}: {str(e)[:80]}")

# Also check SMTP ports
for host, port, label in [
    ("smtp.parleagro.com", 25, "SMTP"),
    ("smtp.parleagro.com", 587, "SMTP-SUB"),
    ("smtp.parleagro.com", 465, "SMTPS"),
    ("imap.parleagro.com", 143, "IMAP"),
    ("imap.parleagro.com", 993, "IMAPS"),
    ("pop3.parleagro.com", 110, "POP3"),
    ("pop3.parleagro.com", 995, "POP3S"),
]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        r = s.connect_ex((host, port))
        s.close()
        if r == 0:
            print(f"{host}:{port} ({label}) - OPEN")
    except:
        pass
