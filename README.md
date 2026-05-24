# Network Monitoring & Chat Application

A complete Python-based client-server application for network monitoring and communication using TCP sockets and JSON messaging.

---

## Project Overview

This application demonstrates:
- **TCP Socket Communication**: Client ↔ Server bidirectional communication
- **JSON Structured Messages**: Standardized data format
- **Threading**: Handle multiple clients simultaneously
- **Network Monitoring**: Ping hosts, scan networks, get IP info
- **GUI Interface**: User-friendly Tkinter-based client
- **Error Handling**: Robust exception handling
- **Logging**: Track all server activities

---

## Architecture

```
┌─────────────────┐         TCP Socket         ┌─────────────────┐
│    Client GUI   │ ──────────────────────────▶ │   TCP Server    │
│  (client.py)    │  JSON Messages (Port 5000) │  (server.py)    │
└─────────────────┘                             └────────┬────────┘
                                                          │
                                                          ▼
                                                  ┌───────────────┐
                                                  │   Utilities   │
                                                  │  (utils.py)   │
                                                  └───────┬───────┘
                                                          │
                                                          ▼
                                                  ┌───────────────┐
                                                  │   Data/Logs   │
                                                  │ (data.json,   │
                                                  │   app.log)    │
                                                  └───────────────┘
```


## How It Works

### 1. Server Side (`server.py`)

**Startup Process**:
1. Creates a TCP socket
2. Binds to `0.0.0.0:5000` (listens on all interfaces)
3. Starts listening for incoming connections
4. Logs startup message to console and `app.log`

**Connection Handling**:
- When a client connects, `server.accept()` accepts the connection
- A new thread is created for each client using `threading.Thread`
- This allows multiple clients to connect simultaneously

**Request Processing (`client_thread` function)**:
1. Receives JSON data from client (up to 4096 bytes)
2. Parses JSON into a Python dictionary
3. Calls `handle_request()` to process the action
4. Sends JSON response back to client
5. Closes the connection

**Supported Actions (`handle_request` function)**:
| Action | Description |
|--------|-------------|
| `chat` | Echoes back the received message |
| `time` | Returns current server datetime |
| `get_data` | Reads and returns data from `data.json` |
| `ping` | Pings a specified host |
| `scan_network` | Scans a subnet for active devices |
| `get_local_ip` | Returns server's local IP address |

---

### 2. Client Side (`client.py`)

**GUI Structure** (3 tabs):
1. **Chat**: Send and receive messages
2. **Network Tools**: Ping, scan network, get local IP
3. **Info**: Get server time and app data

**Core Functionality**:
- `send_request()`: Creates TCP socket, sends JSON request, receives response
- All network operations run in separate threads to keep GUI responsive
- Responses are displayed in appropriate log areas

---

### 3. Utilities (`utils.py`)

| Function | Purpose |
|----------|---------|
| `get_local_ip()` | Detects local IP by connecting to 8.8.8.8 |
| `ping_host()` | Cross-platform ping (Windows: -n, Linux/macOS: -c) |
| `scan_network()` | Scans subnet by pinging each IP from .1 to .254 |
| `load_data()` / `save_data()` | Read/write JSON files |
| `log_message()` | Appends timestamped messages to `app.log` |

---

## Features

✅ **Client ↔ Server Communication** via TCP sockets  
✅ **6+ Request Types**: chat, time, get_data, ping, scan_network, get_local_ip  
✅ **JSON Structured Messages** for standardized data exchange  
✅ **Threading** for multiple concurrent clients  
✅ **Tkinter GUI** with 3 functional tabs  
✅ **Network Monitoring**: Ping hosts, scan local network  
✅ **File I/O**: Read from `data.json`  
✅ **Logging**: All activities logged to `app.log`  
✅ **Error Handling**: Robust try/except blocks  
✅ **Cross-Platform**: Works on Windows, Linux, macOS  

---

## Setup & Installation

### Prerequisites
- Python 3.7+ (download from [python.org](https://www.python.org/))

### Installation Steps

1. **Navigate to project directory**:
    cd NetworkingProject
  

2. **No additional dependencies required** - uses only Python standard library!

---

## How to Use

### Step 1: Start the Server

Open **Terminal 1** and run:
python3 server.py
```

You'll see:
Server started on 0.0.0.0:5000

### Step 2: Start the Client

Open **Terminal 2** and run:
python3 client.py

A GUI window titled "Network Monitoring & Chat App" will open.

### Step 3: Use the Application

The GUI has 3 tabs - let's explore each!

---

## Examples

### Example 1: Chat Feature

1. Go to the **Chat** tab
2. Type a message: `Hello from client!`
3. Click **Send** or press Enter

**What happens behind the scenes**:
1. Client sends JSON:
   ```json
   {
     "action": "chat",
     "data": "Hello from client!"
   }
   ```
2. Server processes and responds:
   ```json
   {
     "status": "success",
     "response": "Server received: Hello from client!"
   }
   ```
3. Client displays both messages in chat log



### Example 2: Ping a Host

1. Go to the **Network Tools** tab
2. In the "Ping Host" field, type: `google.com`
3. Click **Ping**

**What happens**:
1. Client sends:
   ```json
   {
     "action": "ping",
     "host": "google.com"
   }
   ```
2. Server uses `utils.ping_host()` to execute ping command
3. Server returns ping results
4. Client displays:
   ```
   Pinging google.com...
   Ping to google.com successful!
   
   Pinging google.com [142.250.185.46] with 32 bytes of data:
   Reply from 142.250.185.46: bytes=32 time=15ms TTL=118
   Reply from 142.250.185.46: bytes=32 time=14ms TTL=118
   Reply from 142.250.185.46: bytes=32 time=15ms TTL=118
   Reply from 142.250.185.46: bytes=32 time=14ms TTL=118
   
   Ping statistics for 142.250.185.46:
       Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
   Approximate round trip times in milli-seconds:
       Minimum = 14ms, Maximum = 15ms, Average = 14ms
   ```

---

### Example 3: Scan Local Network

1. Go to **Network Tools** tab
2. In "Scan Subnet" field, type your subnet (e.g., `192.168.1`)
3. Click **Scan Network**

**Note**: This may take 1-2 minutes as it pings 254 IP addresses!

**Result**:
```
Scanning network 192.168.1.1-254...
Found 3 devices:
  - 192.168.1.1
  - 192.168.1.10
  - 192.168.1.25



### Example 4: Get Server Time

1. Go to **Info** tab
2. Click **Get Server Time**

**Result**:
```
Server Time: 2026-05-21 14:30:45.123456
```

---

### Example 5: Get App Data

1. Go to **Info** tab
2. Click **Get App Data**

**Result**:
```
App Data: {
  "name": "Network Monitoring & Chat App",
  "version": "1.0",
  "author": "Charles Hemedi",
  "features": [
    "Client-Server TCP Communication",
    "JSON Message Format",
    "Chat Functionality",
    "Network Ping",
    "Network Scan",
    "Local IP Detection",
    "Server Time",
    "Data File Reading",
    "Threading Support",
    "GUI Interface"
  ]
}
```

---

## Message Protocol

### Request Format
All requests from client to server follow this JSON structure:
```json
{
  "action": "action_name",
  "data": "optional_data"
}
```

Additional fields may be included for specific actions (e.g., `host` for ping, `subnet` for scan).

### Response Format
All responses from server to client:
```json
{
  "status": "success",
  "response": "response_data"
}
```

Or for errors:
```json
{
  "status": "error",
  "error": "error message"
}
```

---

## File Structure

```
NetworkingProject/
├── server.py       # TCP Server with threading
├── client.py       # Tkinter GUI Client
├── utils.py        # Networking utilities
├── data.json       # Application data
├── app.log         # Server log file (generated automatically)
└── README.md       # This documentation
```

---

## Troubleshooting

### Issue: "Connection refused" when starting client
**Solution**: Make sure the server is running first!

### Issue: Network scan takes too long
**Solution**: This is normal - it's pinging 254 IPs. You can modify the `start` and `end` parameters in `utils.scan_network()` to scan fewer IPs.

### Issue: Ping doesn't work on Linux/macOS
**Solution**: The code should handle this automatically - it uses `-c` for non-Windows systems.

---

## Networking Concepts Demonstrated

1. **TCP Sockets**: Connection-oriented, reliable communication
2. **Client-Server Architecture**: Central server handles multiple clients
3. **JSON Serialization**: Structured data exchange
4. **Threading**: Concurrent client handling
5. **ICMP (Ping)**: Network layer connectivity testing
6. **IP Subnetting**: Network scanning concepts
7. **Socket Binding/Listening**: Server setup process
8. **Error Handling**: Robust network programming

---

