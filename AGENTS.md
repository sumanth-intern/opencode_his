# Red team / bug bounty workspace

## Commands

All Python scripts are flat, single-file executables with no `if __name__` guard.
They use raw `sys.argv` (no argparse) with hardcoded fallback targets.

```powershell
python 403_bypass.py [target_url]
python deep_scan.py
python check_subdomains.py [domain]
python exposed_files_scanner.py
python stored_xss_tester.py
```

No test, lint, format, typecheck, or build commands exist.

## Dependencies

No `requirements.txt`. Install on demand:

```powershell
pip install requests beautifulsoup4 dnspython
```

## Key conventions

- All Python scripts call `urllib3.disable_warnings()` and use `verify=False`.
- `build.js.map` is the primary source map file for secret extraction via `deep_scan.py`.
- Session notes (`session-*.md`) document real-world engagements in markdown.
- `agents/readme.md` is a REDTEAM-01 operator prompt (injected into LLM context for autonomous red-teaming).
- `opencode_pro.jsonc` is the local opencode config (replaces default `opencode.json`).

## Sensitive data

- `build.js.map`, `ondato_*`, `brup_data.txt`, `vuln_reports.txt`, `report.txt` contain extracted secrets, tokens, and findings.
- `session-*.md` files contain real target URLs and credentials.
- Do not commit or expose these files.
