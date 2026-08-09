package com.benchmark.app;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ProfileServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        // CWE-79: Reflected XSS, user input written into the HTML response unescaped
        String name = req.getParameter("name");
        PrintWriter out = resp.getWriter();
        out.println("<h1>Welcome, " + name + "</h1>");
    }

    protected void doGetSafe(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        // False positive trap: response is escaped before being written
        String name = req.getParameter("name");
        String escaped = name == null ? "" : name
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;");
        resp.getWriter().println("<h1>Welcome, " + escaped + "</h1>");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        // CWE-502: Insecure Deserialization, ObjectInputStream reads untrusted request body
        try {
            ObjectInputStream ois = new ObjectInputStream(req.getInputStream());
            Object session = ois.readObject();
            resp.getWriter().println("Restored: " + session);
        } catch (ClassNotFoundException e) {
            throw new ServletException(e);
        }
    }
}
