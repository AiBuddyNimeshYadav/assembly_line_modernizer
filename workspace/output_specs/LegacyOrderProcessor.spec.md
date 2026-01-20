## Specification: LegacyOrderProcessor

### 1. Overview

This document describes the `LegacyOrderProcessor` Java backend component. Its primary function is to read order data from a specified CSV file, parse the individual order details, sort the orders based on their amount, and generate a processing report. The report maps raw order statuses to a standardized "processed status" and prints a log for each order to the console. The code exhibits several legacy Java programming patterns and practices, which are highlighted within the source comments and detailed in this specification.

### 2. Requirements

#### 2.1 Functional Requirements

*   **F1.0 File Processing**: The system shall read order data from a CSV file specified by a file path.
*   **F1.1 Data Parsing**: For each line in the input file, the system shall parse five fields: Order ID (String), Customer Name (String), Amount (double), Status (String), and Order Date (Date).
*   **F1.2 Date Format**: The order date shall be parsed using the `yyyy-MM-dd` format.
*   **F1.3 Error Handling - Date Parsing**: If a date parsing error occurs for a specific order line, the error shall be printed to the console, and processing shall continue with the next line.
*   **F1.4 Order Storage**: Parsed orders shall be stored in an in-memory list.
*   **F1.5 Order Sorting**: Stored orders shall be sorted in descending order based on their `amount`.
*   **F1.6 Report Generation**: For each sorted order, a processed status shall be determined based on its current status:
    *   "NEW" -> "Processing Initiated"
    *   "SHIPPED" or "DELIVERED" -> "Archived"
    *   "CANCELLED" -> "Refund Processed"
    *   Any other status -> "Manual Review"
*   **F1.7 Report Output**: A log message containing the Order ID and the determined processed status shall be printed to standard output for each order.

#### 2.2 Non-Functional Requirements

*   **NFR1.0 Input Format**: The input file must be a comma-separated values (CSV) file, with each line representing an order and containing exactly five fields in the order: `orderId,customerName,amount,status,orderDate`.
*   **NFR1.1 Error Handling - I/O**: Any `IOException` during file reading or closing shall result in a stack trace being printed to the console.
*   **NFR1.2 Resource Management**: File resources (`BufferedReader`) are manually opened and closed using a `try-finally` block.
*   **NFR1.3 Date Handling Thread Safety**: The `SimpleDateFormat` instance used for date parsing is not thread-safe, implying that concurrent access to `processOrderFile` could lead to issues. (Implicit from code comments)
*   **NFR1.4 Performance (Implicit)**: The code uses string concatenation in a loop, which can be inefficient for large datasets. (Implicit from code comments)

### 3. Technical Details

*   **Language**: Java
*   **Main Class**: `LegacyOrderProcessor`
*   **Data Model**:
    *   `Order` (Inner Static Class): A Plain Old Java Object (POJO) representing an order with fields: `orderId` (String), `customerName` (String), `amount` (double), `status` (String), `orderDate` (Date). It includes a constructor, explicit getters and setters for all fields, and an overridden `toString()` method.
*   **File I/O**:
    *   Uses `java.io.BufferedReader` and `java.io.FileReader` for reading the input CSV file line by line.
    *   Manual resource cleanup is performed in a `finally` block.
*   **Date Handling**:
    *   `java.text.SimpleDateFormat` with pattern `"yyyy-MM-dd"` is used for parsing date strings into `java.util.Date` objects.
*   **Data Structures**:
    *   `java.util.ArrayList<Order>` is used to store orders in memory.
*   **Sorting**:
    *   `java.util.Collections.sort()` is used with an anonymous inner class implementing `java.util.Comparator<Order>` to sort orders by `amount` in descending order.
*   **Iteration**:
    *   An explicit `java.util.Iterator<Order>` is used to traverse the list of orders during report generation.
*   **Status Processing**:
    *   A traditional `switch` statement with explicit `break` statements (including fall-through for "SHIPPED" and "DELIVERED") is used to map order statuses.
*   **String Operations**:
    *   Basic `String.split(",")` for parsing CSV lines.
    *   Direct `+` operator for string concatenation in log messages.
*   **Entry Point**: The `main` method instantiates `LegacyOrderProcessor` and calls `processOrderFile` with a hardcoded example path `"data/orders.csv"`.

#### 3.1 Legacy Aspects (as noted in source code comments)

The code explicitly highlights several patterns considered legacy or suboptimal in modern Java development:

*   **Verbose POJO**: Manual implementation of constructors, getters, setters, and `toString()` for the `Order` class.
*   **Old Date Handling**: Use of `SimpleDateFormat`, which is known to be non-thread-safe and part of the older `java.util.Date` and `java.util.Calendar` API.
*   **Manual Resource Management**: Explicit `try-finally` blocks for closing I/O streams, rather than `try-with-resources`.
*   **Anonymous Inner Classes**: Verbose syntax for implementing `Comparator` for sorting.
*   **Explicit Iterators**: Manual use of `Iterator` for collection traversal.
*   **Fall-through Switch Statement**: Risk of bugs if `break` statements are missed, and generally more verbose than modern alternatives.
*   **String Concatenation**: Use of `+` operator for string building in a loop, which can be inefficient (though often optimized by the compiler for simple cases).
*   **Pre-Java 7 Generics**: The comment `List<Order> orders = new ArrayList<Order>();` notes the explicit type argument for `ArrayList`, which was common before the diamond operator (`<>`) was introduced in Java 7.

### 4. Additional Sections

#### 4.1 Input/Output

*   **Input**: A CSV file (e.g., `data/orders.csv`) containing order records. Each line must conform to the `orderId,customerName,amount,status,orderDate` format.
    *   Example line: `ORD001,John Doe,150.75,NEW,2023-01-15`
*   **Output**: A series of log messages printed to `System.out`, each detailing an order's ID and its processed status.
    *   Example output:
        ```
        --- Processing Report ---
        Order: ORD003 | Action: Archived
        Order: ORD001 | Action: Processing Initiated
        Order: ORD002 | Action: Refund Processed
        ```

#### 4.2 Dependencies

*   Standard Java Development Kit (JDK). No external libraries are used.

#### 4.3 Future Considerations and Modernization Opportunities

Based on the identified legacy aspects, the following improvements could be made to modernize and enhance the `LegacyOrderProcessor`:

*   **Data Model**: Replace the `Order` POJO with a Java Record (Java 16+) for conciseness and immutability.
*   **Date Handling**: Migrate from `SimpleDateFormat` and `java.util.Date` to the `java.time` package (e.g., `LocalDate`, `DateTimeFormatter`) for thread-safe, immutable, and more robust date/time operations.
*   **Resource Management**: Utilize `try-with-resources` statements for automatic closing of `BufferedReader` and other AutoCloseable resources.
*   **Functional Programming**: Leverage Java 8+ features:
    *   Use Lambda expressions for `Comparator` implementations during sorting.
    *   Employ the Stream API for more declarative and efficient data processing, filtering, and mapping operations.
*   **String Building**: Use `StringBuilder` or `StringJoiner` for efficient string concatenation, especially within loops.
*   **Switch Statements**: Consider using enhanced `switch` expressions (Java 14+) for more concise and safer status mapping.
*   **Error Handling**: Implement more sophisticated error logging (e.g., using a logging framework like SLF4J/Logback) instead of `e.printStackTrace()`.
*   **Configuration**: Externalize the input file path (e.g., via command-line arguments, configuration files) instead of hardcoding it.