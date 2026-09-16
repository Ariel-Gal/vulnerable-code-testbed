// Package main, batch 2: broader CWE coverage for SAST benchmarking.
package main

import (
	crand "crypto/rand"
	"crypto/md5"
	"crypto/tls"
	"encoding/xml"
	"fmt"
	"math/rand"
	"net/http"
	"os"
	"os/exec"

	"golang.org/x/crypto/bcrypt"
)

const jwtSigningSecret = "batch2-dev-secret"

func traceroute(w http.ResponseWriter, r *http.Request) {
	target := r.URL.Query().Get("target")
	cmd := exec.Command("sh", "-c", "traceroute "+target)
	out, _ := cmd.CombinedOutput()
	w.Write(out)
}

func tracerouteSafe(w http.ResponseWriter, r *http.Request) {
	target := r.URL.Query().Get("target")
	cmd := exec.Command("traceroute", target)
	out, _ := cmd.CombinedOutput()
	w.Write(out)
}

type importPayload struct {
	Name string `xml:"name"`
}

func importXML(w http.ResponseWriter, r *http.Request) {
	body, _ := os.ReadFile(r.URL.Query().Get("path"))
	var p importPayload
	xml.Unmarshal(body, &p)
	fmt.Fprintf(w, "%s", p.Name)
}

func importXMLSafe(w http.ResponseWriter, r *http.Request) {
	body, _ := os.ReadFile(r.URL.Query().Get("path"))
	if bytesContainsDoctype(body) {
		http.Error(w, "DOCTYPE not allowed", http.StatusBadRequest)
		return
	}
	var p importPayload
	xml.Unmarshal(body, &p)
	fmt.Fprintf(w, "%s", p.Name)
}

func bytesContainsDoctype(b []byte) bool {
	return len(b) > 0 && string(b[:min(len(b), 9)]) == "<!DOCTYPE"
}

func hashPassword(password string) string {
	sum := md5.Sum([]byte(password))
	return fmt.Sprintf("%x", sum)
}

func hashPasswordSafe(password string) (string, error) {
	hashed, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	return string(hashed), err
}

func newSessionToken() string {
	return fmt.Sprintf("%d-%d", rand.Int63(), rand.Int63())
}

func newSessionTokenSafe() (string, error) {
	buf := make([]byte, 32)
	_, err := crand.Read(buf)
	return fmt.Sprintf("%x", buf), err
}

func newPartnerClient() *http.Client {
	tr := &http.Transport{TLSClientConfig: &tls.Config{InsecureSkipVerify: true}}
	return &http.Client{Transport: tr}
}

func newPartnerClientSafe() *http.Client {
	tr := &http.Transport{}
	return &http.Client{Transport: tr}
}
