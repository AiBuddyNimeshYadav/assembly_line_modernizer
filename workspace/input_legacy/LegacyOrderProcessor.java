import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class LegacyOrderProcessor {

    // BLOCK 1: Verbose POJO (Plain Old Java Object)
    // PROBLEM: Requires getters, setters, constructors, and manual toString()
    public static class Order {
        private String orderId;
        private String customerName;
        private double amount;
        private String status;
        private Date orderDate;

        public Order(String orderId, String customerName, double amount, String status, Date orderDate) {
            this.orderId = orderId;
            this.customerName = customerName;
            this.amount = amount;
            this.status = status;
            this.orderDate = orderDate;
        }

        public String getOrderId() { return orderId; }
        public void setOrderId(String orderId) { this.orderId = orderId; }
        public String getCustomerName() { return customerName; }
        public void setCustomerName(String customerName) { this.customerName = customerName; }
        public double getAmount() { return amount; }
        public void setAmount(double amount) { this.amount = amount; }
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        public Date getOrderDate() { return orderDate; }
        public void setOrderDate(Date orderDate) { this.orderDate = orderDate; }

        @Override
        public String toString() {
            return "Order [ID=" + orderId + ", Name=" + customerName + ", Amt=" + amount + ", Status=" + status + "]";
        }
    }

    // BLOCK 2: Old Date Handling & Resource Management
    // PROBLEM: SimpleDateFormat is not thread-safe; try-finally is verbose and error-prone
    public void processOrderFile(String filePath) {
        BufferedReader br = null;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        List<Order> orders = new ArrayList<Order>(); // Diamond operator was new in Java 7, often explicit in older code

        try {
            br = new BufferedReader(new FileReader(filePath));
            String line;

            // Legacy Loop: Reading file line by line
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 5) {
                    // Manual Type Parsing
                    String id = parts[0];
                    String name = parts[1];
                    double amount = Double.parseDouble(parts[2]);
                    String status = parts[3];
                    Date date = null;
                    try {
                        date = sdf.parse(parts[4]);
                    } catch (ParseException e) {
                        e.printStackTrace();
                        continue;
                    }

                    Order order = new Order(id, name, amount, status, date);
                    orders.add(order);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // BLOCK 3: Manual Resource Cleanup
            // PROBLEM: We have to manually close streams in finally block
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        generateReport(orders);
    }

    // BLOCK 4: Anonymous Inner Classes & Explicit Iterators
    // PROBLEM: Verbose syntax for sorting and iteration
    private void generateReport(List<Order> orders) {

        // Sorting using Anonymous Inner Class
        Collections.sort(orders, new Comparator<Order>() {
            @Override
            public int compare(Order o1, Order o2) {
                return Double.compare(o2.getAmount(), o1.getAmount()); // Descending sort
            }
        });

        System.out.println("--- Processing Report ---");

        // Manual Iterator Loop
        Iterator<Order> it = orders.iterator();
        while (it.hasNext()) {
            Order o = it.next();

            // BLOCK 5: Fall-through Switch Statement
            // PROBLEM: Risk of bugs if 'break' is missed; verbose
            String processedStatus = "";
            switch (o.getStatus()) {
                case "NEW":
                    processedStatus = "Processing Initiated";
                    break;
                case "SHIPPED":
                case "DELIVERED":
                    processedStatus = "Archived";
                    break;
                case "CANCELLED":
                    processedStatus = "Refund Processed";
                    break;
                default:
                    processedStatus = "Manual Review";
                    break;
            }

            // BLOCK 6: String Concatenation
            // PROBLEM: Inefficient for large loops (though compiler optimizes simple ones)
            String log = "Order: " + o.getOrderId() + " | Action: " + processedStatus;
            System.out.println(log);
        }
    }

    public static void main(String[] args) {
        LegacyOrderProcessor processor = new LegacyOrderProcessor();
        processor.processOrderFile("data/orders.csv");
    }
}