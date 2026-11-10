#!/usr/bin/env python3
import urllib.request
import json
import os

token = os.environ.get('GITHUB_TOKEN', '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')

repos = ['obrihas2/asda', 'obrihas2/asda']

for repo in repos:
    print("=" * 60)
    print(f"CHECKING {repo}")
    print("=" * 60)
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}/releases?per_page=100')
    req.add_header('User-Agent', 'RoseReleaseTool')
    req.add_header('Authorization', f'token {token}')
    
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode())
        print(f'Total releases: {len(data)}')
        for r in data:
            print(f'  - {r.get("tag_name")}: {r.get("name")}')
            body = r.get("body", "")
            print(f'    Body starts: {str(body)[:80] if body else "empty"}...')
    except urllib.error.HTTPError as e:
        print(f'HTTP Error: {e.code} {e.reason}')
        body = e.read().decode()
        print(f'Body: {body[:200]}')
    print()