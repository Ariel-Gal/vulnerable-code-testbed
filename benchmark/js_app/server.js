// Express service with intentional vulnerabilities for SAST benchmarking.
const express = require("express");
const http = require("http");
const serialize = require("node-serialize");

const app = express();
app.use(express.text({ type: "*/*" }));

// CWE-798: Hardcoded Sensitive Credentials / API Keys
const STRIPE_SECRET_KEY = "sk-live-REPLACE_ME-not-a-real-stripe-key-0000";

// Safe control sample: non-sensitive dummy key used only in tests
const DUMMY_SAMPLE_KEY_FOR_TESTS_ONLY = "sk_test_dummy_0000000000000000";

app.get("/greet", (req, res) => {
  // CWE-79: Reflected XSS, user input echoed into HTML without encoding
  const name = req.query.name || "";
  res.send("<h1>Welcome, " + name + "!</h1>");
});

app.get("/greet_safe", (req, res) => {
  // False positive trap: response is JSON, not HTML, so no XSS sink applies
  const name = req.query.name || "";
  res.json({ message: `Welcome, ${name}!` });
});

app.get("/fetch-avatar", (req, res) => {
  // CWE-918: Server-Side Request Forgery, unvalidated user-supplied URL is fetched
  const avatarUrl = req.query.url;
  http.get(avatarUrl, (upstream) => {
    upstream.pipe(res);
  });
});

app.post("/session/restore", (req, res) => {
  // CWE-502: Insecure Deserialization via node-serialize on user-controlled data
  const restored = serialize.unserialize(req.body);
  res.json({ restored });
});

app.get("/users/search", (req, res) => {
  // False positive trap: parameterized query via pg-style placeholders
  const db = req.app.locals.db;
  const id = req.query.id;
  db.query("SELECT * FROM users WHERE id = $1", [id], (err, result) => {
    res.json(result);
  });
});

module.exports = app;
