// Plain helper functions — no vulnerabilities, pure noise for the scanner.

function slugify(text) {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function formatCurrency(cents) {
  return `$${(cents / 100).toFixed(2)}`;
}

function paginate(items, page, pageSize = 20) {
  const start = Math.max(page - 1, 0) * pageSize;
  return items.slice(start, start + pageSize);
}

function debounce(fn, delayMs) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delayMs);
  };
}

module.exports = { slugify, formatCurrency, paginate, debounce };
