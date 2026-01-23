import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.01"]
  }
};

export default function () {
  const res = http.get("https://test.k6.io");
  check(res, {
    "status is 200": (r) => r.status === 200
  });
  sleep(3);
}
