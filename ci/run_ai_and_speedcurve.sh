#!/usr/bin/env bash
set -euo pipefail

# run AI
python3 ci/ai_call.py --out ai_response.json

# run speedcurve
python3 ci/speedcurve_post.py --input ai_response.json --out speedcurve_response.json
