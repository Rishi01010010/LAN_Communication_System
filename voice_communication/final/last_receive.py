import socket
import threading
import pyaudio
import sys

# Configuration
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 50020
DISCOVERY_PORT = 50021  # Port for device discovery
BUFFER_SIZE = 4096  # Size of incoming audio chunks

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

username = input("Enter your username: ")

def respond_to_discovery():
    """
    Listens for discovery messages and responds to the sender with the username.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, DISCOVERY_PORT))

    print(f"[DISCOVERY] Starting device discovery for 10 seconds...")
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        if data.decode('utf-8') == "DISCOVER_RECEIVER":
            response = f"{username} at {addr[0]}"
            print(f"[DISCOVERY] Found device with IP adress {addr[0]}")
            sock.sendto(username.encode('utf-8'), addr)

def handle_connection_request():
    """
    Listens for incoming connection requests and handles them.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((UDP_IP, DISCOVERY_PORT))
    sock.listen(1)

    print(f"[LISTENING] Client listening on port {DISCOVERY_PORT}...")

    conn, addr = sock.accept()
    print(f"[REQUEST] Connection request from {addr}")

    data = conn.recv(BUFFER_SIZE).decode('utf-8')
    if data == "REQUEST_CONNECTION":
        decision = input(f"Do you want to accept the connection from {addr}? (yes/no): ").strip().lower()
        if decision == 'yes':
            conn.sendall("ACCEPT".encode('utf-8'))
            return addr[0]  # Return the sender's IP address
        else:
            conn.sendall("REJECT".encode('utf-8'))
            return None
    conn.close()

def receive_voice():
    """
    Receives audio data over UDP and plays it through the speakers.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"[VOICE RECEIVER] Listening for voice on UDP port {UDP_PORT}")

    # Set up PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            stream.write(data)
    except KeyboardInterrupt:
        print("\n[VOICE RECEIVER] Stopping voice reception.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        sock.close()


if __name__ == "__main__":
    # Step 1: Start a thread to listen for discovery messages
    discovery_thread = threading.Thread(target=respond_to_discovery, daemon=True)
    discovery_thread.start()

    # Step 2: Wait for a connection request
    sender_ip = handle_connection_request()

    # Step 3: Start receiving voice if the connection is accepted
    if sender_ip:
        receive_voice()
    else:
        print("[INFO] Connection was not accepted.")
