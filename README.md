
# Request Rate Limiter Simulation

This project simulates a **priority-based, rate-limited request processing system**, showcasing how requests are prioritized and processed by multiple providers with configurable rate limits. It emphasizes thread-safe queue management and controlled request handling.

----------

## Features

1.  **Request Management**:
    
    -   Requests have an ID, priority, and timestamp.
    -   Higher priority requests are processed first, with older requests taking precedence when priorities are equal.
2.  **Customizable Providers**:
    
    -   Providers simulate processing threads with user-defined rate limits (requests per second).
3.  **Thread-Safe Queue**:
    
    -   Safely manages request additions and retrievals across multiple threads.
4.  **Random Priority Testing**:
    
    -   Each request is assigned a random priority (1–3) to simulate varying urgency levels and test the priority-based system effectively.

----------

## Components Overview

### 1. **`Request` Class**

Represents a request with:

-   **ID**: Unique identifier.
-   **Priority**: Randomly assigned for testing purposes (1 = lowest, 3 = highest).
-   **Timestamp**: Captures the time the request is received.

### 2. **`RequestQueue` Class**

A thread-safe priority queue that:

-   Ensures higher priority requests are processed first.
-   Resolves ties in priority by processing older requests first.

### 3. **`Provider` Class**

Represents a processing thread that:

-   Fetches and processes requests from the queue.
-   Operates at a defined rate limit (e.g., 0.2 requests/second = 1 request every 5 seconds).

### 4. **`main` Function**

Manages the simulation:

-   Prompts the user to configure providers and generate requests.
-   Keeps the program running using the `sleep` function to ensure that all requests are processed by the providers before the application exits. This ensures the simulation completes without premature termination.

----------

## Example Output

**Providers and Requests**:

-   Provider P1 (0.5 requests/second)
-   Provider P2 (0.2 requests/second)
-   Generated requests with random priorities.

**Sample Output**:

```plaintext
[2024-01-01 10:00:00] P1 processing Request(id=1, priority=3)
[2024-01-01 10:00:05] P2 processing Request(id=2, priority=2)
[2024-01-01 10:00:10] P1 processing Request(id=3, priority=1)
...