#!/usr/bin/env python3
import os, sys, json, argparse, requests

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='ai_response.json')
parser.add_argument('--out', default='speedcurve_response.json')
args = parser.parse_args()

SPEEDCURVE_KEY = os.getenv('SPEEDCURVE_KEY')
SPEEDCURVE_SITE = os.getenv('SPEEDCURVE_SITE_ID')
SPEEDCURVE_API_URL = os.getenv('SPEEDCURVE_API_URL', 'https://api.speedcurve.com/v1')  # placeholder

if not SPEEDCURVE_KEY or not SPEEDCURVE_SITE:
    print("SPEEDCURVE_KEY or SPEEDCURVE_SITE_ID not set", file=sys.stderr)
    sys.exit(1)

# read the AI response (optional)
ai = {}
if os.path.exists(args.input):
    ai = json.load(open(args.input))

# Example: post a synthetic test run. Replace with the real SpeedCurve endpoint.
payload = {
    "site_id": SPEEDCURVE_SITE,
    "notes": "Triggered by CI pipeline. AI summary: " + (ai.get('choices', [{}])[0].get('message', {}).get('content','')[:200] if ai else "")
}

headers = {
    "Authorization": f"Bearer {SPEEDCURVE_KEY}",
    "Content-Type": "application/json"
}

# Example endpoint path — adjust to real SpeedCurve API endpoints your team uses:
url = f"{SPEEDCURVE_API_URL}/sites/{SPEEDCURVE_SITE}/runs"

r = requests.post(url, json=payload, headers=headers, timeout=60)
# if they use a different endpoint, update 'url' variable
try:
    r.raise_for_status()
    result = r.json()
except Exception as e:
    result = {"error": str(e), "status_code": getattr(r, "status_code", None), "text": r.text}

with open(args.out, 'w') as f:
    json.dump(result, f, indent=2)

print("SpeedCurve response saved to", args.out)
