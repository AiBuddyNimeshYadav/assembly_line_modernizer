package com.example.controller;

import javax.faces.bean.ManagedBean;
import javax.faces.bean.ViewScoped;
import javax.annotation.PostConstruct;
import java.util.ArrayList;
import java.util.List;
import java.util.Date;

@ManagedBean
@ViewScoped
public class UserController {

    private List<User> users;
    private User selectedUser;
    private String searchTerm;

    @PostConstruct
    public void init() {
        users = new ArrayList<>();
        loadUsers();
    }

    public void loadUsers() {
        // Simulate loading users from database
        users.add(new User(1L, "John Doe", "john@example.com", new Date()));
        users.add(new User(2L, "Jane Smith", "jane@example.com", new Date()));
    }

    public String saveUser() {
        if (selectedUser != null) {
            // Save logic here
            System.out.println("Saving user: " + selectedUser.getName());
        }
        return "success";
    }

    public void deleteUser(User user) {
        users.remove(user);
    }

    public void searchUsers() {
        if (searchTerm != null && !searchTerm.isEmpty()) {
            // Filter users by search term
            System.out.println("Searching for: " + searchTerm);
        }
    }

    // Getters and Setters
    public List<User> getUsers() {
        return users;
    }

    public void setUsers(List<User> users) {
        this.users = users;
    }

    public User getSelectedUser() {
        return selectedUser;
    }

    public void setSelectedUser(User selectedUser) {
        this.selectedUser = selectedUser;
    }

    public String getSearchTerm() {
        return searchTerm;
    }

    public void setSearchTerm(String searchTerm) {
        this.searchTerm = searchTerm;
    }
}

class User {
    private Long id;
    private String name;
    private String email;
    private Date createdDate;

    public User(Long id, String name, String email, Date createdDate) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdDate = createdDate;
    }

    // Getters and setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Date getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(Date createdDate) {
        this.createdDate = createdDate;
    }
}
