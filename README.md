# K6 + Kubernetes + CircleCI pipeline

## What this repo contains
- `.circleci/config.yml` - CircleCI pipeline
- `k8s/k6-job.yaml` - Kubernetes Job that runs k6
- `k6/test.js` - sample k6 script
- `ci/ai_call.py` - example AI call script (reads OPENAI_KEY)
- `ci/speedcurve_post.py` - example SpeedCurve post (reads SPEEDCURVE_KEY)

## Required CircleCI project environment variables
Set these in the CircleCI project settings -> Environment Variables:
- KUBE_CONFIG_DATA : base64 encoded kubeconfig (cat ~/.kube/config | base64 | tr -d '\n')
- OPENAI_KEY : OpenAI API key (or provider key)
- OPENAI_API_URL : (optional) AI endpoint URL if non-default
- SPEEDCURVE_KEY : SpeedCurve API key
- SPEEDCURVE_SITE_ID : SpeedCurve site identifier
- SPEEDCURVE_API_URL : (optional) base API URL for SpeedCurve

## How pipeline works
1. Checkout repo
2. Restore kubeconfig and connect to cluster
3. Apply `k8s/k6-job.yaml` (runs k6 in cluster)
4. Wait for pod and capture logs (saved as artifact)
5. Run AI step (ci/ai_call.py)
6. Run SpeedCurve step (ci/speedcurve_post.py)
7. Artifacts (k6 log, AI response, SpeedCurve response) are stored in CircleCI

## Notes
- For EKS, you can generate kubeconfig with `aws eks update-kubeconfig` and then set `KUBE_CONFIG_DATA`.
- For SpeedCurve API specifics, provide exact API docs / credentials to integrate precisely.

## My Notes

