package com.example.controller;

import com.example.dto.UserDTO;
import com.example.service.UserService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public ResponseEntity<List<UserDTO>> getAllUsers() {
        List<UserDTO> users = userService.findAllUsers();
        return ResponseEntity.ok(users);
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUserById(@PathVariable Long id) {
        return userService.findUserById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<UserDTO> createUser(@Valid @RequestBody UserDTO userDTO) {
        UserDTO savedUser = userService.saveUser(userDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedUser);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserDTO> updateUser(@PathVariable Long id, @Valid @RequestBody UserDTO userDTO) {
        if (!userService.findUserById(id).isPresent()) {
            return ResponseEntity.notFound().build();
        }
        UserDTO updatedUser = userService.updateUser(id, userDTO);
        return ResponseEntity.ok(updatedUser);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        if (userService.deleteUser(id)) {
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }

    @GetMapping("/search")
    public ResponseEntity<List<UserDTO>> searchUsers(@RequestParam @NotBlank String searchTerm) {
        List<UserDTO> foundUsers = userService.searchUsers(searchTerm);
        return ResponseEntity.ok(foundUsers);
    }
}

package com.example.service;

import com.example.dto.UserDTO;
import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import java.util.stream.Collectors;

@Service
public class UserService {

    private final Map<Long, UserDTO> users = new ConcurrentHashMap<>();
    private final AtomicLong idCounter = new AtomicLong();

    @PostConstruct
    public void init() {
        // Simulate loading users from database
        saveUser(new UserDTO(null, "John Doe", "john@example.com", Instant.now()));
        saveUser(new UserDTO(null, "Jane Smith", "jane@example.com", Instant.now()));
        saveUser(new UserDTO(null, "Peter Jones", "peter@example.com", Instant.now()));
    }

    public List<UserDTO> findAllUsers() {
        return new ArrayList<>(users.values());
    }

    public Optional<UserDTO> findUserById(Long id) {
        return Optional.ofNullable(users.get(id));
    }

    public UserDTO saveUser(UserDTO userDTO) {
        Long id = userDTO.id() != null ? userDTO.id() : idCounter.incrementAndGet();
        UserDTO newUser = new UserDTO(id, userDTO.name(), userDTO.email(), userDTO.createdDate() != null ? userDTO.createdDate() : Instant.now());
        users.put(id, newUser);
        return newUser;
    }

    public UserDTO updateUser(Long id, UserDTO userDTO) {
        if (!users.containsKey(id)) {
            throw new IllegalArgumentException("User with ID " + id + " not found.");
        }
        UserDTO updatedUser = new UserDTO(id, userDTO.name(), userDTO.email(), userDTO.createdDate() != null ? userDTO.createdDate() : users.get(id).createdDate());
        users.put(id, updatedUser);
        return updatedUser;
    }

    public boolean deleteUser(Long id) {
        return users.remove(id) != null;
    }

    public List<UserDTO> searchUsers(String searchTerm) {
        String lowerCaseSearchTerm = searchTerm.toLowerCase();
        return users.values().stream()
                .filter(user -> user.name().toLowerCase().contains(lowerCaseSearchTerm) ||
                                 user.email().toLowerCase().contains(lowerCaseSearchTerm))
                .collect(Collectors.toList());
    }
}

package com.example.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.Instant;

public record UserDTO(
    Long id,
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    String name,
    @NotBlank(message = "Email is required")
    @Email(message = "Email should be valid")
    String email,
    Instant createdDate
) {}