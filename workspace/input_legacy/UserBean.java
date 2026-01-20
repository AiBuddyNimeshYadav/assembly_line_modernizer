package com.legacy.beans;

import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import com.legacy.service.UserService;

@ManagedBean
@SessionScoped
public class UserBean {

    private UserService userService; // Dependency
    private String username;

    public void deleteUser(String id) {
        userService.delete(id);
    }
    
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
}
