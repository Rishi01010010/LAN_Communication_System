import socket
import threading
import pyaudio
import sys
import time

# Configuration
UDP_PORT = 50020
BUFFER_SIZE = 1024  # Size of outgoing audio chunks
DISCOVERY_PORT = 50021  # Port for discovering devices

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

username = input("Enter your username: ")

def discover_devices():
    """
    Broadcasts a message on the network to discover active receivers.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(10)  # Wait for 2 seconds for responses

    message = "DISCOVER_RECEIVER"
    print("[DISCOVERY] Starting device discovery for 10 seconds...")
    sock.sendto(message.encode('utf-8'), ('<broadcast>', DISCOVERY_PORT))

    start_time = time.time()
    devices = []
    while time.time() - start_time < 10:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            devices.append((data.decode('utf-8'), addr[0]))
            print(f"[DISCOVERY] Found device '{data.decode('utf-8')}' at {addr[0]}")
        except socket.timeout:
            break
    sock.close()

    return devices

def send_request(target_ip):
    """
    Sends a connection request to the receiver and waits for an acceptance.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((target_ip, DISCOVERY_PORT))
        print(f"[REQUEST] Sending connection request to {target_ip}...")
        sock.sendall("REQUEST_CONNECTION".encode('utf-8'))

        response = sock.recv(BUFFER_SIZE).decode('utf-8')
        if response == "ACCEPT":
            print("[CONNECTED] Connected to client at {target_ip}")
            return True
        else:
            print("[REJECTED] Connection rejected by the client.")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to connect to {target_ip}: {e}")
        return False
    finally:
        sock.close()

def send_voice(target_ip):
    """
    Captures audio from the microphone and sends it over UDP.
    """
    # Set up UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[VOICE SENDER] Sending voice to {target_ip}:{UDP_PORT}. Press Ctrl+C to stop.")

    # Set up PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    try:
        while True:
            data = stream.read(CHUNK)
            sock.sendto(data, (target_ip, UDP_PORT))
    except KeyboardInterrupt:
        print("\n[VOICE SENDER] Stopping voice transmission.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        sock.close()

if __name__ == "__main__":
    # Step 1: Discover devices on the network
    devices = discover_devices()

    if devices:
        print("\n[DISCOVERY] Devices found:")
        print("-------------------------")
        for idx, (name, ip) in enumerate(devices):
            print(f"{idx + 1}. {name} - {ip}")
        print("-------------------------")

        # Allow user to select or exit
        target_ip = input("Enter the client's IP address to connect (or type 'exit' to quit): ").strip()
        if target_ip.lower() == 'exit':
            print("[INFO] Exiting.")
            sys.exit()

        # Step 2: Send connection request to the selected device
        if send_request(target_ip):
            # Step 3: Start voice communication if accepted
            send_voice(target_ip)
        else:
            print("[INFO] Communication terminated.")
    else:
        print("[ERROR] No devices found.")
        sys.exit()
