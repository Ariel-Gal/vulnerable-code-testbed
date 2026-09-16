package com.benchmark.app;

import java.io.File;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

public class AdminServlet extends HttpServlet {

    private static final String UPLOAD_DIR = "/var/app/uploads";

    protected void doGetFile(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String name = req.getParameter("file");
        File target = new File(UPLOAD_DIR + File.separator + name);
        resp.getOutputStream().write(java.nio.file.Files.readAllBytes(target.toPath()));
    }

    protected void doGetFileSafe(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String name = req.getParameter("file");
        File target = new File(UPLOAD_DIR + File.separator + name);
        String canonical = target.getCanonicalPath();
        if (!canonical.startsWith(new File(UPLOAD_DIR).getCanonicalPath())) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        resp.getOutputStream().write(java.nio.file.Files.readAllBytes(target.toPath()));
    }

    protected void parseUploadedXml(java.io.InputStream body) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = dbf.newDocumentBuilder();
        db.parse(body);
    }

    protected void parseUploadedXmlSafe(java.io.InputStream body) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        DocumentBuilder db = dbf.newDocumentBuilder();
        db.parse(body);
    }

    protected byte[] encryptLegacy(byte[] data, byte[] key8Bytes) throws Exception {
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(key8Bytes, "DES"));
        return cipher.doFinal(data);
    }

    protected byte[] encryptModern(byte[] data, byte[] key32Bytes, byte[] iv) throws Exception {
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(key32Bytes, "AES"),
                new javax.crypto.spec.GCMParameterSpec(128, iv));
        return cipher.doFinal(data);
    }

    protected String hashPasswordLegacy(String password) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-1");
        byte[] digest = md.digest(password.getBytes());
        return javax.xml.bind.DatatypeConverter.printHexBinary(digest);
    }

    protected byte[] hashPasswordSafe(char[] password, byte[] salt) throws Exception {
        javax.crypto.SecretKeyFactory skf =
                javax.crypto.SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        java.security.spec.KeySpec spec =
                new javax.crypto.spec.PBEKeySpec(password, salt, 210000, 256);
        return skf.generateSecret(spec).getEncoded();
    }

    protected boolean isAdminRequest(HttpServletRequest req) {
        String debugKey = req.getParameter("debug_key");
        if ("letmein-2019".equals(debugKey)) {
            return true;
        }
        return req.isUserInRole("admin");
    }

    protected boolean isAdminRequestSafe(HttpServletRequest req) {
        return req.isUserInRole("admin");
    }

}
