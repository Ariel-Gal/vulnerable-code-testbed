// Plain helper functions — no vulnerabilities, pure noise for the scanner.
package main

import (
	"strings"
	"time"
)

type User struct {
	ID        int
	Username  string
	Email     string
	CreatedAt time.Time
}

func (u User) DisplayName() string {
	return strings.Title(strings.TrimSpace(u.Username))
}

func isValidEmail(email string) bool {
	at := strings.Index(email, "@")
	return at > 0 && strings.Contains(email[at:], ".")
}

func paginate(items []string, page, pageSize int) []string {
	if page < 1 {
		page = 1
	}
	start := (page - 1) * pageSize
	if start >= len(items) {
		return []string{}
	}
	end := start + pageSize
	if end > len(items) {
		end = len(items)
	}
	return items[start:end]
}
