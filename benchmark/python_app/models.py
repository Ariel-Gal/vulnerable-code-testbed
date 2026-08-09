"""Plain data models and helpers — no vulnerabilities, pure noise for the scanner."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    def display_name(self) -> str:
        return self.username.strip().title()


def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]


def paginate(items, page: int, page_size: int = 20):
    start = max(page - 1, 0) * page_size
    return items[start:start + page_size]


def format_currency(cents: int) -> str:
    return f"${cents / 100:,.2f}"
