#!/usr/bin/env python3
import os, sys, json, argparse, requests

parser = argparse.ArgumentParser()
parser.add_argument('--out', default='ai_response.json')
args = parser.parse_args()

OPENAI_KEY = os.getenv('OPENAI_KEY') or os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_KEY')
if not OPENAI_KEY:
    print("OPENAI_KEY not set", file=sys.stderr)
    sys.exit(1)

# Example: call OpenAI-compatible API endpoint (chat completions)
API_URL = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1/chat/completions')

payload = {
    "model": "gpt-4o-mini",   # change as needed
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Generate a short summary of the k6 results and a SpeedCurve test URL to run next."}
    ],
    "max_tokens": 200
}

headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}

r = requests.post(API_URL, json=payload, headers=headers, timeout=60)
r.raise_for_status()
resp = r.json()

# Keep the full response for debugging
with open(args.out, 'w') as f:
    json.dump(resp, f, indent=2)

print("AI response saved to", args.out)
