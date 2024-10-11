# host.py
import socket
import threading
import time
import sys

# Configuration for Messaging
MESSAGING_PORT = 50010  # Port for TCP messaging
BUFFER_SIZE = 1024      # Maximum size of incoming messages

# Configuration for Device Discovery
BROADCAST_PORT = 50000
BROADCAST_INTERVAL = 5  # seconds
DISCOVERY_DURATION = 10 # seconds to discover devices
BUFFER_SIZE_DISCOVERY = 1024

def broadcast_presence(username):
    """
    Broadcasts the host's presence to the network periodically.
    """
    broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = f"DISCOVERY:{username}".encode('utf-8')
    while not stop_event.is_set():
        try:
            broadcaster.sendto(message, ('<broadcast>', BROADCAST_PORT))
            # print(f"[BROADCAST] Sent discovery message: {message.decode('utf-8')}")
        except Exception as e:
            print(f"[ERROR] Broadcasting failed: {e}")
        time.sleep(BROADCAST_INTERVAL)
    broadcaster.close()

def listen_for_devices(my_username, known_devices):
    """
    Listens for discovery broadcasts from other devices and updates known_devices.
    """
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(('', BROADCAST_PORT))
    listener.settimeout(DISCOVERY_DURATION + BROADCAST_INTERVAL)  # Timeout after discovery period
    while not stop_event.is_set():
        try:
            data, addr = listener.recvfrom(BUFFER_SIZE_DISCOVERY)
            message = data.decode('utf-8')
            if message.startswith("DISCOVERY:"):
                username = message.split(":", 1)[1]
                if addr[0] not in known_devices and username != my_username:
                    print(f"[DISCOVERY] Found device '{username}' at {addr[0]}")
                    known_devices[addr[0]] = username
        except socket.timeout:
            # Discovery period ended
            break
        except Exception as e:
            print(f"[ERROR] Listening for devices failed: {e}")
            break
    listener.close()

def receive_messages(sock):
    """
    Listens for incoming messages from the client and prints them.
    """
    while True:
        try:
            message = sock.recv(BUFFER_SIZE).decode('utf-8')
            if not message:
                # Client has closed the connection
                print("[INFO] Client disconnected.")
                break
            print(f"Client: {message}")
        except ConnectionResetError:
            print("[ERROR] Connection lost.")
            break
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
            break
    sock.close()
    sys.exit()

def send_messages(sock):
    """
    Sends messages to the client.
    """
    try:
        while True:
            message = input()
            if message.lower() == 'exit':
                print("[INFO] Disconnecting from client.")
                break
            if message.strip() == '':
                continue  # Ignore empty messages
            sock.sendall(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("\n[INFO] Keyboard interrupt received. Disconnecting.")
    finally:
        sock.close()
        print("[INFO] Disconnected from client.")
        sys.exit()

def start_host():
    """
    Initiates device discovery, allows user to select a client, and facilitates messaging upon acceptance.
    """
    global stop_event
    stop_event = threading.Event()

    # Input Username for Discovery
    my_username = input("Enter your username: ").strip()
    if not my_username:
        my_username = "Host"

    # Dictionary to store discovered devices: {IP: Username}
    known_devices = {}

    # Start broadcasting thread
    broadcaster_thread = threading.Thread(target=broadcast_presence, args=(my_username,), daemon=True)
    broadcaster_thread.start()

    # Start listening thread
    listener_thread = threading.Thread(target=listen_for_devices, args=(my_username, known_devices), daemon=True)
    listener_thread.start()

    print(f"[DISCOVERY] Starting device discovery for {DISCOVERY_DURATION} seconds...")
    time.sleep(DISCOVERY_DURATION)

    # Stop broadcasting after discovery period
    stop_event.set()
    broadcaster_thread.join()
    listener_thread.join()

    if not known_devices:
        print("[DISCOVERY] No devices found on the network.")
    else:
        print("\n[DISCOVERY] Devices found:")
        print("-------------------------")
        for idx, (ip, username) in enumerate(known_devices.items(), start=1):
            print(f"{idx}. {username} - {ip}")
        print("-------------------------\n")

    # Prompt user to select a client by IP
    while True:
        client_ip = input("Enter the client's IP address to connect (or type 'exit' to quit): ").strip()
        if client_ip.lower() == 'exit':
            print("[INFO] Exiting the host.")
            sys.exit()
        elif client_ip in known_devices:
            break
        else:
            print("[WARNING] Invalid IP address. Please enter a valid IP from the discovered devices.")

    client_port = MESSAGING_PORT  # Must match the client's listening port

    # Attempt to connect to the selected client
    host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_sock.connect((client_ip, client_port))
        print(f"[CONNECTED] Connected to client '{known_devices[client_ip]}' at {client_ip}:{client_port}")
    except Exception as e:
        print(f"[ERROR] Could not connect to client: {e}")
        sys.exit()

    try:
        # Wait for the client's response to the connection request
        response = host_sock.recv(BUFFER_SIZE).decode('utf-8')
        if response == "ACCEPT":
            print("[INFO] Connection accepted by the client. You can start chatting.")
        elif response == "REJECT":
            print("[INFO] Connection rejected by the client.")
            host_sock.close()
            sys.exit()
        else:
            print(f"[INFO] Received unexpected response: {response}")
            host_sock.close()
            sys.exit()
    except Exception as e:
        print(f"[ERROR] Failed to receive response from client: {e}")
        host_sock.close()
        sys.exit()

    # Start threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(host_sock,), daemon=True)
    send_thread = threading.Thread(target=send_messages, args=(host_sock,), daemon=True)
    receive_thread.start()
    send_thread.start()

    # Wait for threads to finish
    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":
    start_host()
