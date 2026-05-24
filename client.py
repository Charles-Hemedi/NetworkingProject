import socket
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

# Client configuration
HOST = '127.0.0.1'  # Server address (localhost)
PORT = 5000          # Server port

class NetworkApp:
    """
    Main application class for the Network Monitoring & Chat App GUI.
    """
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Network Monitoring & Chat App")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        """Create the main GUI widgets including the tabbed interface."""
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create Chat tab
        chat_frame = ttk.Frame(notebook)
        notebook.add(chat_frame, text='Chat')
        self.create_chat_tab(chat_frame)

        # Create Network Tools tab
        network_frame = ttk.Frame(notebook)
        notebook.add(network_frame, text='Network Tools')
        self.create_network_tab(network_frame)

        # Create Info tab
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text='Info')
        self.create_info_tab(info_frame)

    def create_chat_tab(self, parent):
        """
        Create the Chat tab interface.
        
        Args:
            parent: Parent frame widget
        """
        # Chat log display area
        self.chat_log = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=20)
        self.chat_log.pack(expand=True, fill='both', padx=5, pady=5)

        # Input area
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill='x', padx=5, pady=5)

        self.chat_input = ttk.Entry(input_frame)
        self.chat_input.pack(side='left', expand=True, fill='x', padx=5)
        self.chat_input.bind('<Return>', lambda e: self.send_chat())  # Allow Enter key to send

        send_btn = ttk.Button(input_frame, text='Send', command=self.send_chat)
        send_btn.pack(side='right', padx=5)

    def create_network_tab(self, parent):
        """
        Create the Network Tools tab interface.
        
        Args:
            parent: Parent frame widget
        """
        tools_frame = ttk.LabelFrame(parent, text='Network Tools')
        tools_frame.pack(fill='x', padx=5, pady=5)

        # Ping tool
        ping_frame = ttk.Frame(tools_frame)
        ping_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(ping_frame, text='Ping Host:').pack(side='left')
        self.ping_input = ttk.Entry(ping_frame)
        self.ping_input.pack(side='left', expand=True, fill='x', padx=5)
        self.ping_input.insert(0, '8.8.8.8')  # Default: Google DNS
        ttk.Button(ping_frame, text='Ping', command=self.ping_host).pack(side='left')

        # Network scan tool
        scan_frame = ttk.Frame(tools_frame)
        scan_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(scan_frame, text='Scan Subnet:').pack(side='left')
        self.scan_input = ttk.Entry(scan_frame)
        self.scan_input.pack(side='left', expand=True, fill='x', padx=5)
        self.scan_input.insert(0, '192.168.1')  # Default subnet
        ttk.Button(scan_frame, text='Scan Network', command=self.scan_network).pack(side='left')

        # Local IP button
        ttk.Button(tools_frame, text='Get Local IP', command=self.get_local_ip).pack(pady=5)

        # Network log display area
        self.network_log = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=15)
        self.network_log.pack(expand=True, fill='both', padx=5, pady=5)

    def create_info_tab(self, parent):
        """
        Create the Info tab interface.
        
        Args:
            parent: Parent frame widget
        """
        # Info log display area
        self.info_log = scrolledtext.ScrolledText(parent, wrap=tk.WORD)
        self.info_log.pack(expand=True, fill='both', padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text='Get Server Time', command=self.get_server_time).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Get App Data', command=self.get_app_data).pack(side='left', padx=5)

    def send_request(self, action, data=None):
        """
        Sends a JSON request to the server and returns the response.
        
        Args:
            action (str): Request action type
            data: Optional data to send with request
        
        Returns:
            dict: Server response
        """
        try:
            # Create TCP socket and connect to server
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))

            # Build request
            request = {"action": action, "data": data}
            if action == "ping":
                request["host"] = data
            if action == "scan_network":
                request["subnet"] = data

            # Send request and receive response
            client.send(json.dumps(request).encode())
            response = client.recv(4096).decode()
            client.close()

            return json.loads(response)
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def log_to(self, widget, message):
        """
        Appends a message to a text widget and scrolls to the end.
        
        Args:
            widget: Text widget to log to
            message (str): Message to log
        """
        widget.insert(tk.END, message + '\n')
        widget.see(tk.END)

    def send_chat(self):
        """Sends a chat message to the server (runs in separate thread)."""
        msg = self.chat_input.get()
        if not msg:
            return

        # Display user message
        self.log_to(self.chat_log, f"You: {msg}")
        self.chat_input.delete(0, tk.END)

        def send():
            """Thread function to send request without blocking GUI."""
            response = self.send_request("chat", msg)
            if response.get("status") == "success":
                self.log_to(self.chat_log, f"Server: {response['response']}")
            else:
                self.log_to(self.chat_log, f"Error: {response.get('error', 'Unknown error')}")

        threading.Thread(target=send).start()

    def ping_host(self):
        """Pings a host (runs in separate thread)."""
        host = self.ping_input.get()
        self.log_to(self.network_log, f"Pinging {host}...")

        def ping():
            """Thread function to ping host without blocking GUI."""
            response = self.send_request("ping", host)
            if response.get("status") == "success":
                result = response['response']
                if result['success']:
                    self.log_to(self.network_log, f"Ping to {host} successful!\n{result['output']}")
                else:
                    self.log_to(self.network_log, f"Ping to {host} failed!")
            else:
                self.log_to(self.network_log, f"Error: {response.get('error', 'Unknown error')}")

        threading.Thread(target=ping).start()

    def scan_network(self):
        """Scans a network subnet (runs in separate thread)."""
        subnet = self.scan_input.get()
        self.log_to(self.network_log, f"Scanning network {subnet}.1-254...")

        def scan():
            """Thread function to scan network without blocking GUI."""
            response = self.send_request("scan_network", subnet)
            if response.get("status") == "success":
                devices = response['response']
                self.log_to(self.network_log, f"Found {len(devices)} devices:")
                for device in devices:
                    self.log_to(self.network_log, f"  - {device}")
            else:
                self.log_to(self.network_log, f"Error: {response.get('error', 'Unknown error')}")

        threading.Thread(target=scan).start()

    def get_local_ip(self):
        """Gets the server's local IP address."""
        response = self.send_request("get_local_ip")
        if response.get("status") == "success":
            self.log_to(self.network_log, f"Local IP: {response['response']}")
        else:
            self.log_to(self.network_log, f"Error: {response.get('error', 'Unknown error')}")

    def get_server_time(self):
        """Gets the current server time."""
        response = self.send_request("time")
        if response.get("status") == "success":
            self.log_to(self.info_log, f"Server Time: {response['response']}")
        else:
            self.log_to(self.info_log, f"Error: {response.get('error', 'Unknown error')}")

    def get_app_data(self):
        """Gets application data from data.json file."""
        response = self.send_request("get_data")
        if response.get("status") == "success":
            self.log_to(self.info_log, f"App Data: {json.dumps(response['response'], indent=2)}")
        else:
            self.log_to(self.info_log, f"Error: {response.get('error', 'Unknown error')}")

if __name__ == "__main__":
    # Create and run the GUI application
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()
