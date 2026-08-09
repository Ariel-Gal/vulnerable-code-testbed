// Package main implements a REST API with intentional vulnerabilities for SAST benchmarking.
package main

import (
	"database/sql"
	"fmt"
	"net/http"
	"os/exec"
	"path/filepath"
	"strings"

	_ "github.com/mattn/go-sqlite3"
)

// CWE-798: Hardcoded Sensitive Credentials / API Keys
const dbPassword = "prod-db-p@ssw0rd-2024"

// Safe control sample: non-sensitive dummy key used only in tests
const dummySampleKeyForTestsOnly = "dummy-0000000000000000"

const uploadDir = "./uploads"

var db *sql.DB

func searchUsers(w http.ResponseWriter, r *http.Request) {
	// CWE-89: SQL Injection via string concatenation
	username := r.URL.Query().Get("username")
	query := "SELECT id, email FROM users WHERE username = '" + username + "'"
	rows, _ := db.Query(query)
	defer rows.Close()
	fmt.Fprintf(w, "%v", rows)
}

func searchUsersSafe(w http.ResponseWriter, r *http.Request) {
	// False positive trap: parameterized query
	username := r.URL.Query().Get("username")
	rows, _ := db.Query("SELECT id, email FROM users WHERE username = ?", username)
	defer rows.Close()
	fmt.Fprintf(w, "%v", rows)
}

func pingHost(w http.ResponseWriter, r *http.Request) {
	// CWE-78: OS Command Injection, user input passed straight to a shell
	host := r.URL.Query().Get("host")
	cmd := exec.Command("sh", "-c", "ping -c 1 "+host)
	out, _ := cmd.CombinedOutput()
	w.Write(out)
}

func readFile(w http.ResponseWriter, r *http.Request) {
	// CWE-22: Path Traversal / Arbitrary File Read
	name := r.URL.Query().Get("name")
	http.ServeFile(w, r, filepath.Join(uploadDir, name))
}

func readFileSafe(w http.ResponseWriter, r *http.Request) {
	// False positive trap: resolved path is verified to stay under uploadDir
	name := r.URL.Query().Get("name")
	absBase, _ := filepath.Abs(uploadDir)
	resolved, _ := filepath.Abs(filepath.Join(uploadDir, name))
	if !strings.HasPrefix(resolved, absBase+string(filepath.Separator)) {
		http.Error(w, "invalid path", http.StatusBadRequest)
		return
	}
	http.ServeFile(w, r, resolved)
}

func main() {
	http.HandleFunc("/users/search", searchUsers)
	http.HandleFunc("/users/search_safe", searchUsersSafe)
	http.HandleFunc("/ping", pingHost)
	http.HandleFunc("/files", readFile)
	http.HandleFunc("/files_safe", readFileSafe)
	http.ListenAndServe(":8080", nil)
}
