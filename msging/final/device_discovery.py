import socket
import threading
import time

# Configuration
BROADCAST_PORT = 50000
BROADCAST_INTERVAL = 5  # seconds
BUFFER_SIZE = 1024

# Function to broadcast presence
def broadcast_presence(username):
    broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = f"DISCOVERY:{username}".encode('utf-8')
    while True:
        broadcaster.sendto(message, ('<broadcast>', BROADCAST_PORT))
        time.sleep(BROADCAST_INTERVAL)

# Function to listen for other devices
def listen_for_devices(my_username, known_devices):
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(('', BROADCAST_PORT))
    while True:
        data, addr = listener.recvfrom(BUFFER_SIZE)
        message = data.decode('utf-8')
        if message.startswith("DISCOVERY:"):
            username = message.split(":")[1]
            if addr[0] not in known_devices and username != my_username:
                print(f"Discovered {username} at {addr[0]}")
                known_devices[addr[0]] = username

if __name__ == "__main__":
    my_username = input("Enter your username: ")
    known_devices = {}

    # Start broadcasting thread
    broadcaster_thread = threading.Thread(target=broadcast_presence, args=(my_username,), daemon=True)
    broadcaster_thread.start()

    # Start listening thread
    listener_thread = threading.Thread(target=listen_for_devices, args=(my_username, known_devices), daemon=True)
    listener_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting device discovery.")
