package com.benchmark.app;

// Plain helper functions — no vulnerabilities, pure noise for the scanner.
public final class StringUtils {

    private StringUtils() {
    }

    public static String slugify(String text) {
        if (text == null) {
            return "";
        }
        return text.trim().toLowerCase().replaceAll("[^a-z0-9]+", "-").replaceAll("(^-|-$)", "");
    }

    public static boolean isValidEmail(String email) {
        if (email == null) {
            return false;
        }
        int at = email.indexOf('@');
        return at > 0 && email.substring(at).contains(".");
    }

    public static String formatCurrency(long cents) {
        return String.format("$%,.2f", cents / 100.0);
    }
}
