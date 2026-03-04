package com.example.vulnerable;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;

@RestController
public class FileController {

    @GetMapping("/download")
    public String downloadFile(@RequestParam String filename) {
        try {
            return new String(Files.readAllBytes(Paths.get("uploads/" + filename)));
        } catch (IOException e) {
            return "Error";
        }
    }
}