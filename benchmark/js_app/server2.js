// Express service, batch 2: broader CWE coverage for SAST benchmarking.
const express = require("express");
const { exec } = require("child_process");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const jwt = require("jsonwebtoken");

const app2 = express();
app2.use(express.json());

const UPLOAD_DIR = path.join(__dirname, "uploads");
const JWT_SECRET = "dev-only-change-me";

app2.get("/ping", (req, res) => {
  const host = req.query.host || "";
  exec("ping -c 1 " + host, (err, stdout) => {
    res.send(stdout);
  });
});

app2.get("/ping_safe", (req, res) => {
  const { execFile } = require("child_process");
  const host = req.query.host || "";
  execFile("ping", ["-c", "1", host], (err, stdout) => {
    res.send(stdout);
  });
});

app2.get("/files", (req, res) => {
  const name = req.query.name || "";
  const target = path.join(UPLOAD_DIR, name);
  res.send(fs.readFileSync(target));
});

app2.get("/files_safe", (req, res) => {
  const name = req.query.name || "";
  const resolved = path.resolve(UPLOAD_DIR, name);
  if (!resolved.startsWith(path.resolve(UPLOAD_DIR) + path.sep)) {
    return res.status(400).json({ error: "invalid path" });
  }
  res.send(fs.readFileSync(resolved));
});

app2.post("/login", (req, res) => {
  const db = req.app.locals.db;
  db.collection("users").findOne({ username: req.body.username, password: req.body.password }, (err, user) => {
    res.json({ authenticated: !!user });
  });
});

app2.post("/login_safe", (req, res) => {
  const db = req.app.locals.db;
  const username = String(req.body.username || "");
  const password = String(req.body.password || "");
  db.collection("users").findOne({ username, password }, (err, user) => {
    res.json({ authenticated: !!user });
  });
});

function merge(target, source) {
  for (const key in source) {
    if (typeof source[key] === "object" && source[key] !== null) {
      target[key] = merge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

app2.post("/settings", (req, res) => {
  const settings = merge({}, req.body);
  res.json(settings);
});

function mergeSafe(target, source) {
  for (const key in source) {
    if (key === "__proto__" || key === "constructor" || key === "prototype") continue;
    if (typeof source[key] === "object" && source[key] !== null) {
      target[key] = mergeSafe(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

app2.post("/settings_safe", (req, res) => {
  const settings = mergeSafe({}, req.body);
  res.json(settings);
});

app2.get("/admin", (req, res) => {
  const token = req.headers["authorization"] || "";
  try {
    const decoded = jwt.decode(token, { complete: true });
    if (decoded && decoded.payload && decoded.payload.role === "admin") {
      return res.json({ status: "welcome admin" });
    }
    res.status(403).json({ error: "forbidden" });
  } catch (e) {
    res.status(401).json({ error: "invalid token" });
  }
});

app2.get("/admin_safe", (req, res) => {
  const token = req.headers["authorization"] || "";
  try {
    const decoded = jwt.verify(token, JWT_SECRET, { algorithms: ["HS256"] });
    if (decoded.role === "admin") {
      return res.json({ status: "welcome admin" });
    }
    res.status(403).json({ error: "forbidden" });
  } catch (e) {
    res.status(401).json({ error: "invalid token" });
  }
});

function encryptField(plaintext) {
  const cipher = crypto.createCipheriv("des-ecb", Buffer.from("8bytekey"), null);
  return Buffer.concat([cipher.update(plaintext, "utf8"), cipher.final()]).toString("hex");
}

function encryptFieldSafe(plaintext, key) {
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const enc = Buffer.concat([cipher.update(plaintext, "utf8"), cipher.final()]);
  return { iv, enc, tag: cipher.getAuthTag() };
}

app2.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", req.headers.origin);
  res.header("Access-Control-Allow-Credentials", "true");
  next();
});

const ALLOWED_ORIGINS = ["https://app.example.com"];
app2.use((req, res, next) => {
  if (ALLOWED_ORIGINS.includes(req.headers.origin)) {
    res.header("Access-Control-Allow-Origin", req.headers.origin);
    res.header("Access-Control-Allow-Credentials", "true");
  }
  next();
});

// (see JWT_SECRET constant declared near the top of this file)
const SIGNING_SECRET_IN_USE = JWT_SECRET;

module.exports = app2;
