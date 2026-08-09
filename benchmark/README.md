# AppSec Benchmark Target

Multi-language ground-truth benchmark for evaluating SAST tools / AI security agents.
See [`../benchmark_manifest.json`](../benchmark_manifest.json) for the ground truth
(15 true-positive vulnerabilities, 10 false-positive traps) and
[`../evaluate_agent.py`](../evaluate_agent.py) to score a report against it.

```
benchmark/
  python_app/app.py          Flask: SQLi, command injection, path traversal, hardcoded creds, pickle deserialization (+ safe controls)
  js_app/server.js           Express: XSS, SSRF, node-serialize deserialization, hardcoded creds (+ safe controls)
  go_app/main.go             net/http: SQLi, command injection, path traversal (+ safe controls)
  java_app/.../UserDao.java  JDBC: SQLi via Statement (+ PreparedStatement control)
  java_app/.../ProfileServlet.java  Servlet: reflected XSS, ObjectInputStream deserialization (+ escaped-output control)

  python_app/models.py       plain data models/helpers, no vulnerabilities — scanner noise
  js_app/utils.js            plain helper functions, no vulnerabilities — scanner noise
  go_app/helpers.go          plain helper functions, no vulnerabilities — scanner noise
  java_app/.../StringUtils.java  plain helper functions, no vulnerabilities — scanner noise
```

The four "noise" files above are deliberately mundane, realistic-looking business logic with
zero vulnerabilities. They're not in `benchmark_manifest.json` (nothing to detect there) — their
purpose is to make the codebase less obviously "100% malicious code," a truer test of whether a
scanner flags things that were never flagged as findings in the first place.

## Usage

```bash
python evaluate_agent.py benchmark_manifest.json <your_agent_report>.json   # or .sarif
```

`benchmark/sample_appsec_report.json` is a worked example (5 correct hits, 1 false alarm)
used as this project's self-check — run the command above against it to confirm the
scorer computes the expected 83.33% precision / 33.33% recall / 47.62% F1.

⚠️ All code in `benchmark/` is intentionally vulnerable. Never deploy it.
