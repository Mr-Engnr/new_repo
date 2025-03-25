[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/b9MT3x4-)
# Test Harness for Reliable Transport

This README provides a detailed guide for using the **Test Harness for Reliable Transport Protocols**. It includes test descriptions, instructions on how to run the tests, and details on verbose logging, particularly for the `WindowSize` test, which is designed for **Selective Repeat Protocol**. Additionally, it explains how outputs are handled and how to manually clean up if necessary.

---

## **Table of Contents**

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Features](#features)
4. [How to Run](#how-to-run)
5. [Command-Line Arguments](#command-line-arguments)
6. [Test Cases](#test-cases)
7. [Verbose Logging](#verbose-logging)
8. [WindowSize Test Specifics](#windowsize-test-specifics)
9. [Output Handling](#output-handling)
10. [Understanding Test Results](#understanding-test-results)
11. [Troubleshooting](#troubleshooting)

---

## **Overview**

The Test Harness validates transport protocol implementations for reliability, efficiency, and correctness under various network conditions, such as packet loss, duplication, and reordering. It supports multiple tests and provides detailed logging for debugging. 

**All commands detailed here assumed your Current Directory is `Code`.**

## **Features**

- **Automated Cleanup**: Deletes previous test outputs automatically on each run.
- **Verbose Logging**: Provides packet-level debugging insights.
- **Manual Cleanup Support**: Allows manual cleanup of previous outputs if needed.
- **Automated Code Quality Review:** Use Radon to automate code quality grading

---

## **How to Run**

Run the test harness using the following command:

```bash
python3 TestHarness.py [options]
```

### Examples:

Run all tests with verbose logging:

```bash
python3 TestHarness.py --client client.py --server server.py --verbose
```

Run specific tests (e.g., BasicFunctionality and PacketLoss):

```bash
python3 TestHarness.py --tests BasicFunctionality PacketLoss --verbose
```

---

## **Command-Line Arguments**

| Argument              | Description                                                                     | Default       |
| --------------------- | ------------------------------------------------------------------------------- | ------------- |
| `-p`, `--port`    | Base port value for communication. If not provided, a random port will be used. | Random Port   |
| `-c`, `--client`  | Path to the client (sender) implementation.                                     | `client.py` |
| `-s`, `--server`  | Path to the server (receiver) implementation.                                   | `server.py` |
| `-t`, `--tests`   | Space-separated list of tests to run. Multiple tests can be specified.          | All Tests     |
| `-v`, `--verbose` | Enables verbose logging, providing detailed debugging information.              | Disabled      |
| `-h`, `--help`    | Display usage instructions.                                                     | -             |

---

## **Test Cases**

### 1. **BasicFunctionalityTest**

- **Objective:** Verifies basic communication between sender and receiver.
- **Checks:**
  - Sender sends data to the receiver.
  - Receiver processes and outputs data correctly.
- **Command:**
  ```bash
  python3 TestHarness.py --tests BasicFunctionality
  ```

### 2. **PacketLossTest**

- **Objective:** Tests the protocol's ability to handle packet loss.
- **Checks:**
  - Sender retransmits lost packets.
  - Receiver reconstructs the message correctly.
- **Command:**
  ```bash
  python3 TestHarness.py --tests PacketLoss
  ```

### 3. **DuplicatePacketsTest**

- **Objective:** Ensures the protocol can handle duplicate packets.
- **Checks:**
  - Duplicate packets are ignored by the receiver.
  - Final message matches the original.
- **Command:**
  ```bash
  python3 TestHarness.py --tests DuplicatePackets
  ```

### 4. **OutOfOrderPacketsTest**

- **Objective:** Verifies the protocol's ability to handle out-of-order delivery.
- **Checks:**
  - Receiver reorders packets correctly.
  - Final output matches the expected message.
- **Command:**
  ```bash
  python3 TestHarness.py --tests OutOfOrderPackets
  ```

### 5. **WindowSizeTest (Selective Repeat)**

- **Objective:** Evaluates adherence to sliding window protocols, particularly **Selective Repeat**.
- **Checks:**
  - The number of in-flight packets adheres to the window size.
  - Correct handling of ACKs and retransmissions.
  - Retransmissions are selective (**Selective Repeat behavior**).
- **Command:**
  ```bash
  python3 TestHarness.py --tests WindowSize
  ```

## **Concurrency and Performance**

The `TestHarness.py` script leverages **threading** to achieve significant speed improvements in running tests. By executing multiple tests in parallel, the harness makes efficient use of system resources, dramatically reducing overall runtime.

---

#### **Performance Impact**

- **Sequential Execution**: Running all tests one after the other previously took **1 minute and 44 seconds**.
- **Concurrent Execution**: Using threading, the total runtime was reduced to just **22 seconds**.
- **Speed-Up Achieved**: This improvement represents a **4.7x speed-up**! 🤯

---

#### **Performance Comparison**

| **Metric**         | **Sequential** | **Concurrent (Threading)** | **Improvement** |
| ------------------------ | -------------------- | -------------------------------- | --------------------- |
| **Total Runtime**  | 1m 44s               | 22s                              | **4.7x Faster** |
| **Resource Usage** | Low                  | High                             | Efficient Use         |
| **Test Execution** | One-at-a-time        | Parallel                         | Drastically Reduced   |

---

## **Verbose Logging**

Enable verbose logging with the `--verbose` flag for detailed debugging information.

### **What Does Verbose Logging Show?**

1. **Basic Tests:**

   - Shows expected client and server outputs.
   - Highlights missing or mismatched lines.
2. **WindowSize Test:**

   - Detailed packet-level logging:
     - Packets sent.
     - ACKs received.
     - In-flight packets.
     - Updates to the sender’s sliding window.
   - Validates:
     - Adherence to the window size.
     - Retransmissions occur only when necessary.
     - Sliding window functionality.

#### **Example Output:**

```plaintext
Testing WindowSize

Debugging for User: client1
Extracted Packets:
{1: ['data1', 'data2'], 5: ['data3', 'data4', 'data5']}
Iterating Through Packets...
Packet 1: Type: start, Seq No: 1
  - Start Packet Detected. Packets to Send: 2
Packet 2: Type: ack, Seq No: 2
  - ACK Packet Detected. Max Sent: 2
  - Window size fully utilized.

...
```

---

## **WindowSize Test Specifics**

### **Selective Repeat Protocol:**

- **WindowSize Test** is designed specifically for **Selective Repeat Protocol**:
  - The protocol must independently acknowledge packets.
  - Retransmissions are selective and do not reset the entire window.
- The test will fail for **Go-Back-N** due to its cumulative ACK behavior.

### **How It Works:**

1. Tracks packets between `start` and `end`.
2. Validates:
   - The number of in-flight packets matches the window size (or fewer if fewer packets remain).
   - Sliding window advances as ACKs are received.
3. Logs detailed insights for debugging:
   - Packets sent in each window.
   - ACKs received and updates to the window.

---

## **Output Handling**

### **Automatic Cleanup:**

- Each test run deletes previous outputs to ensure clean runs.
- Deleted files:
  - `client_*`
  - `test_*`
  - `*_test_*`
  - `server_out*`

### **Manual Cleanup:**

To manually delete previous outputs, run:

```bash
python3 -c "from TestHarness import delete_with_rm_rf; delete_with_rm_rf()"

# or 

rm -rf ./client_* ./test_* ./*_test_* ./server_out*
```

---

## **Understanding Test Results**

### **Pass/Fail Status:**

- Each test displays "Test Passed!" or "Test Failed!".
- Failures include detailed logs (with `--verbose`) to help debug issues.

### **Final Score:**

- The harness calculates a final score out of 35, with each test contributing 5 points while WindowSIze test contirbuting 10 and 5 marks for Code quality.
- Example:
  ```
  Final Score: 25/35
  ```

---

## **Troubleshooting**

1. **Timeout Errors:**

   - Ensure your implementation correctly handles ACKs, timeouts, and retransmissions.
   - Check for infinite loops.
2. **Verbose Logging:**

   - Use the `--verbose` flag for packet-level debugging.
3. **Output Files Missing:**

   - Ensure the harness has the necessary permissions to create and delete files.

## Code Quality Check

### Overview

**`ReviewCodeQuality.py`** ensures the code adheres to standards of:

- **Maintainability**
- **Modularity**
- **Cyclomatic Complexity**
- **Comments Documentation**

It evaluates files using tools like **Radon** and **Pylint**, scoring them on various metrics.

### Metrics and Scoring

1. **Maintainability Index (MI)**

   - Scored using Radon:
     - Grade A/B: **1 point**
     - Grade C: **0.75 points**
     - Grade D: **0.5 points**
     - Grade E: **0.25 points**
     - Grade F: **0.1 points**
2. **Cyclomatic Complexity (CC)**

   - Graded by Radon:
     - Grade A/B: **1 point**
     - Grade C: **0.75 points**
     - Grade D: **0.5 points**
     - Grade E: **0.25 points**
     - Grade F: **0.1 points**
3. **Pylint Score**

   - Scaled to **2.5 points**:
     - 8–10: **2.5 points**
     - 7–7.9: **2 points**
     - 5–6.9: **1.5 points**
     - 3–4.9: **1 point**
     - Below 3: **0.5 points**
4. **Comments Ratio**

   - Based on percentage of comments in the code:
     - ≥15%: **0.5 points**
     - 10–14.9%: **0.45 points**
     - 5–9.9%: **0.35 points**
     - 2–4.9%: **0.25 points**
     - <2%: **0.1 points**

---

### Running Code Quality Checks

```bash
python3 ReviewCodeQuality.py <file_paths>
```

#### Example

```bash
python3 ReviewCodeQuality.py reliable_transport.py util.py
```

### Output Example

```bash
Processing: reliable_transport.py
Results for client.py:
  Modularity: 1/1
  Cyclomatic Complexity: 1/1
  Pylint Rating: 2/2.5
  Comments Ratio: 0.45/0.5
  Final Score: 4.95/5

Processing: util.py
Results for client.py:
  Modularity: 1/1
  Cyclomatic Complexity: 1/1
  Pylint Rating: 2/2.5
  Comments Ratio: 0.45/0.5
  Final Score: 4.95/5

Average Score for 2 file(s): 5/5
```

---

## Docker Setup

A **Dockerfile** is included for consistent testing. Use the following steps:

1. **Build and Run Container**:

   ```bash
   docker compose run --rm netcen-spring-2025
   # or
   docker-compose run --rm netcen-spring-2025
   ```

   **What this command does**:

   - **`run`**: Executes the `netcen-spring-2025` service defined in the `docker-compose.yml` file as a temporary, one-off container.
   - **`--rm`**: Automatically removes the container after the task completes, ensuring no leftover containers clutter the system.
   - This command starts the container and runs the service or command specified for `netcen-spring-2025` in `docker-compose.yml`.
2. **Access Code**:

   - Code is mounted at `/home/netcen_pa2` inside the container. This allows you to access and work with your files directly within the container.

## Dependencies

Ensure the following dependencies are installed. These are also frozen into `requirements.txt` in `Code` folder.

- Python 3.10+
- `radon`, `pylint`

Install dependencies:

```bash
pip install radon pylint

pip install -r requirements.txt
```

For documentation:

- [Radon Documentation](https://radon.readthedocs.io/en/latest/)
- [Pylint Documentation](https://pylint.readthedocs.io/en/stable/user_guide/)

Happy Testing! 🚀
