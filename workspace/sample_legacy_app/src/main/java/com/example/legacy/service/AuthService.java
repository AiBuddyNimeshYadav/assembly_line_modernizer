package com.example.legacy.service;

public class AuthService {

    public boolean authenticate(String username, String password) {
        // Hardcoded for legacy demo
        return "admin".equals(username) && "password".equals(password);
    }
}
