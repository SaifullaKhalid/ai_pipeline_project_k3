import time
import os, json, requests

key = os.getenv("SPEEDCURVE_KEY")
site = os.getenv("SPEEDCURVE_SITE_ID")

url = "https://api.speedcurve.com/v1/deploys"
auth = (key, "")
payload = {
    "site_id": site,
    "note": "CircleCI trigger"
}

def trigger_deploy():
    resp = requests.post(url, auth=auth, json=payload)
    if resp.status_code == 403:
        print("Deploy in progress. Waiting 90 seconds...")
        time.sleep(90)
        return trigger_deploy()  # retry
    return resp

resp = trigger_deploy()

with open("speedcurve_response.json", "w") as f:
    json.dump({"status": resp.status_code, "body": resp.text}, f, indent=2)

print("Done.")
