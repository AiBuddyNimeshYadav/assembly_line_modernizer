package com.example.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.time.LocalDate;

public record OrderDTO(
    @NotBlank String orderId,
    @NotBlank String customerName,
    @Positive double amount,
    @NotBlank String status,
    @NotNull LocalDate orderDate
) {}

package com.example.dto;

public record ReportEntryDTO(
    String orderId,
    String action
) {}

package com.example.service;

import com.example.dto.OrderDTO;
import com.example.dto.ReportEntryDTO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Service
@RequiredArgsConstructor
public class OrderService {

    public List<OrderDTO> processOrderLines(List<String> orderLines) {
        return orderLines.stream()
                .map(this::parseOrderLine)
                .flatMap(Stream::ofNullable)
                .collect(Collectors.toList());
    }

    private OrderDTO parseOrderLine(String line) {
        String[] parts = line.split(",");
        if (parts.length == 5) {
            try {
                String id = parts[0];
                String name = parts[1];
                double amount = Double.parseDouble(parts[2]);
                String status = parts[3];
                LocalDate date = LocalDate.parse(parts[4]);

                return new OrderDTO(id, name, amount, status, date);
            } catch (NumberFormatException | DateTimeParseException e) {
                System.err.println("Error parsing order line: " + line + " - " + e.getMessage());
                return null;
            }
        }
        return null;
    }

    public List<ReportEntryDTO> generateOrderReport(List<OrderDTO> orders) {
        List<OrderDTO> sortedOrders = orders.stream()
                .sorted(Comparator.comparingDouble(OrderDTO::amount).reversed())
                .collect(Collectors.toList());

        System.out.println("--- Processing Report ---");

        return sortedOrders.stream()
                .map(this::createReportEntry)
                .collect(Collectors.toList());
    }

    private ReportEntryDTO createReportEntry(OrderDTO order) {
        String processedStatus = switch (order.status()) {
            case "NEW" -> "Processing Initiated";
            case "SHIPPED", "DELIVERED" -> "Archived";
            case "CANCELLED" -> "Refund Processed";
            default -> "Manual Review";
        };

        String log = String.format("Order: %s | Action: %s", order.orderId(), processedStatus);
        System.out.println(log);

        return new ReportEntryDTO(order.orderId(), processedStatus);
    }
}

package com.example.controller;

import com.example.dto.OrderDTO;
import com.example.dto.ReportEntryDTO;
import com.example.service.OrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @PostMapping("/process-file")
    public ResponseEntity<List<ReportEntryDTO>> processOrderFile(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        List<String> orderLines;
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(file.getInputStream()))) {
            orderLines = reader.lines().collect(Collectors.toList());
        } catch (IOException e) {
            System.err.println("Failed to read uploaded file: " + e.getMessage());
            return ResponseEntity.internalServerError().build();
        }

        List<OrderDTO> orders = orderService.processOrderLines(orderLines);
        List<ReportEntryDTO> report = orderService.generateOrderReport(orders);
        return ResponseEntity.ok(report);
    }
}

package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}