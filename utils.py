import socket
import subprocess
import platform
import json
from datetime import datetime

def get_local_ip():
    """
    Detects the local IP address of the machine by connecting to an external server.
    
    Returns:
        str: Local IP address, or 127.0.0.1 if detection fails
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def ping_host(host, count=4):
    """
    Pings a specified host using the system ping command.
    
    Args:
        host (str): Hostname or IP address to ping
        count (int): Number of ping packets to send (default: 4)
    
    Returns:
        dict: Contains host, success status, and output/error
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), host]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        return {
            "host": host,
            "success": result.returncode == 0,
            "output": result.stdout
        }
    except Exception as e:
        return {
            "host": host,
            "success": False,
            "error": str(e)
        }

def scan_network(subnet, start=1, end=254):
    """
    Scans a network subnet for active devices by pinging each IP address.
    
    Args:
        subnet (str): Network subnet (e.g., "192.168.1")
        start (int): Starting IP suffix (default: 1)
        end (int): Ending IP suffix (default: 254)
    
    Returns:
        list: List of active IP addresses
    """
    devices = []
    for i in range(start, end + 1):
        ip = f"{subnet}.{i}"
        result = ping_host(ip, count=1)
        if result["success"]:
            devices.append(ip)
    return devices

def load_data(filename="data.json"):
    """
    Loads JSON data from a file.
    
    Args:
        filename (str): Path to JSON file (default: "data.json")
    
    Returns:
        dict: Loaded data, or empty dict if file not found
    """
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data, filename="data.json"):
    """
    Saves data to a JSON file.
    
    Args:
        data (dict): Data to save
        filename (str): Path to JSON file (default: "data.json")
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def log_message(message, filename="app.log"):
    """
    Appends a timestamped message to a log file.
    
    Args:
        message (str): Message to log
        filename (str): Path to log file (default: "app.log")
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
