import socket
import json
import threading
from datetime import datetime
import utils

# Server configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5000        # Port to listen on

# Create and configure TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
server.bind((HOST, PORT))
server.listen()

print(f"Server started on {HOST}:{PORT}")
utils.log_message(f"Server started on {HOST}:{PORT}")

def handle_request(request, addr):
    """
    Handles incoming client requests and returns appropriate responses.
    
    Args:
        request (dict): JSON request from client containing 'action' and optional data
        addr (tuple): Client address (IP, port)
    
    Returns:
        dict: Response with status and response/error data
    """
    action = request.get("action")
    utils.log_message(f"Received {action} request from {addr}")

    try:
        if action == "chat":
            # Echo chat message back to client
            return {"status": "success", "response": f"Server received: {request['data']}"}

        elif action == "time":
            # Return current server time
            return {"status": "success", "response": str(datetime.now())}

        elif action == "get_data":
            # Load and return data from data.json file
            data = utils.load_data()
            return {"status": "success", "response": data}

        elif action == "ping":
            # Ping a specified host
            host = request.get("host", "8.8.8.8")
            result = utils.ping_host(host)
            return {"status": "success", "response": result}

        elif action == "scan_network":
            # Scan a network subnet for active devices
            subnet = request.get("subnet", "192.168.1")
            devices = utils.scan_network(subnet)
            return {"status": "success", "response": devices}

        elif action == "get_local_ip":
            # Get server's local IP address
            ip = utils.get_local_ip()
            return {"status": "success", "response": ip}

        else:
            # Handle unknown actions
            return {"status": "error", "error": "Unknown action"}

    except Exception as e:
        # Handle any unexpected errors
        utils.log_message(f"Error handling request: {str(e)}")
        return {"status": "error", "error": str(e)}

def client_thread(conn, addr):
    """
    Handles communication with a single client in a separate thread.
    
    Args:
        conn: Socket connection object
        addr (tuple): Client address (IP, port)
    """
    print(f"Connected to {addr}")
    utils.log_message(f"Connected to {addr}")
    
    try:
        # Receive and decode JSON request from client
        data = conn.recv(4096).decode()
        request = json.loads(data)
        
        # Process the request and get response
        response = handle_request(request, addr)
        
        # Send JSON response back to client
        conn.send(json.dumps(response).encode())
        
    except Exception as e:
        # Handle errors during communication
        error_response = {"status": "error", "error": str(e)}
        conn.send(json.dumps(error_response).encode())
        utils.log_message(f"Error with client {addr}: {str(e)}")
    
    finally:
        # Always close the connection
        conn.close()
        print(f"Disconnected from {addr}")
        utils.log_message(f"Disconnected from {addr}")

# Main server loop - accept incoming connections indefinitely
while True:
    conn, addr = server.accept()
    # Start a new thread for each client
    threading.Thread(target=client_thread, args=(conn, addr)).start()
