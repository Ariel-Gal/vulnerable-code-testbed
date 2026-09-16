# AppSec Benchmark Target

Multi-language ground-truth benchmark for evaluating SAST tools / AI security agents.
See [`../benchmark_manifest.json`](../benchmark_manifest.json) for the ground truth
(67 true-positive vulnerabilities, 61 false-positive traps, across Python, JavaScript,
Go, Java, PHP and Ruby) and [`../evaluate_agent.py`](../evaluate_agent.py) to score a
report against it.

```
benchmark/
  python_app/app.py          Flask: SQLi, command injection, path traversal, hardcoded creds, pickle deserialization (+ safe controls)
  python_app/app2.py         Flask batch 2: SSRF, XXE, unsafe YAML, SSTI, open redirect, weak crypto, insecure randomness,
                              code injection (eval), zip slip, ReDoS, insecure cookies, cert-verification bypass, IDOR, log
                              injection of secrets (+ safe controls for each)
  js_app/server.js           Express: XSS, SSRF, node-serialize deserialization, hardcoded creds (+ safe controls)
  js_app/server2.js          Express batch 2: command injection, path traversal, NoSQL injection, prototype pollution,
                              forged JWT (alg confusion), broken crypto (DES), permissive CORS w/ credentials (+ safe controls)
  go_app/main.go             net/http: SQLi, command injection, path traversal (+ safe controls)
  go_app/main2.go            net/http batch 2: command injection, XXE, weak password hash (MD5), insecure randomness,
                              disabled TLS verification (+ safe controls)
  java_app/.../UserDao.java  JDBC: SQLi via Statement (+ PreparedStatement control)
  java_app/.../ProfileServlet.java  Servlet: reflected XSS, ObjectInputStream deserialization (+ escaped-output control)
  java_app/.../AdminServlet.java    Servlet batch 2: path traversal, XXE, broken crypto (DES), weak password hash (SHA-1),
                              hardcoded debug backdoor (+ safe controls)
  php_app/index.php          Plain PHP: SQLi, command injection, LFI, XSS, insecure deserialization, path traversal, XXE,
                              weak password hash, insecure randomness, open redirect (+ safe controls)
  ruby_app/app.rb            Sinatra-style: SQLi, command injection, path traversal, Marshal/YAML deserialization, weak
                              password hash, insecure randomness, mass assignment (+ safe controls)

  python_app/models.py       plain data models/helpers, no vulnerabilities — scanner noise
  js_app/utils.js            plain helper functions, no vulnerabilities — scanner noise
  go_app/helpers.go          plain helper functions, no vulnerabilities — scanner noise
  java_app/.../StringUtils.java  plain helper functions, no vulnerabilities — scanner noise
```

The "noise" files above are deliberately mundane, realistic-looking business logic with
zero vulnerabilities. They're not in `benchmark_manifest.json` (nothing to detect there) — their
purpose is to make the codebase less obviously "100% malicious code," a truer test of whether a
scanner flags things that were never flagged as findings in the first place.

## Usage

```bash
python evaluate_agent.py benchmark_manifest.json <your_agent_report>.json   # or .sarif
```

`benchmark/sample_appsec_report.json` is a small worked example (5 correct hits, 1 false
alarm from the original core manifest) used as this project's self-check — run the command
above against it to confirm the scorer computes 83.33% precision / 7.46% recall / 13.70% F1
against the full (post-expansion) manifest.

⚠️ All code in `benchmark/` is intentionally vulnerable. Never deploy it.
