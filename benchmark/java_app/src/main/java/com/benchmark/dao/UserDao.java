package com.benchmark.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class UserDao {

    // CWE-798: Hardcoded Sensitive Credentials / API Keys
    private static final String DB_PASSWORD = "prod-mysql-p@ss-2024";

    // Safe control sample: non-sensitive dummy key used only in tests
    private static final String DUMMY_SAMPLE_KEY_FOR_TESTS_ONLY = "dummy-0000000000000000";

    public ResultSet findByUsername(Connection conn, String username) throws SQLException {
        // CWE-89: SQL Injection via string concatenation
        Statement stmt = conn.createStatement();
        String query = "SELECT id, email FROM users WHERE username = '" + username + "'";
        return stmt.executeQuery(query);
    }

    public ResultSet findByUsernameSafe(Connection conn, String username) throws SQLException {
        // False positive trap: PreparedStatement with bound parameter
        PreparedStatement stmt = conn.prepareStatement(
                "SELECT id, email FROM users WHERE username = ?");
        stmt.setString(1, username);
        return stmt.executeQuery();
    }
}
