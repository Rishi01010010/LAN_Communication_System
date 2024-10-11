import socket
import pyaudio
import threading
import time

# Configuration
BROADCAST_PORT = 50000
UDP_PORT = 50020
BUFFER_SIZE = 1024  # Size of outgoing audio chunks

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Function to broadcast presence
def broadcast_presence(username):
    broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = f"DISCOVERY:{username}".encode('utf-8')
    while True:
        broadcaster.sendto(message, ('<broadcast>', BROADCAST_PORT))
        time.sleep(5)

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

def send_voice(target_ips):
    """
    Captures audio from the microphone and sends it over UDP to multiple target IPs.
    """
    # Set up UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[VOICE SENDER] Sending voice to {', '.join(target_ips)}:{UDP_PORT}. Press Ctrl+C to stop.")

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
            for target_ip in target_ips:
                sock.sendto(data, (target_ip, UDP_PORT))
    except KeyboardInterrupt:
        print("\n[VOICE SENDER] Stopping voice transmission.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        sock.close()

if __name__ == "__main__":
    my_username = input("Enter your username: ")
    known_devices = {}

    # Start broadcasting thread
    broadcaster_thread = threading.Thread(target=broadcast_presence, args=(my_username,), daemon=True)
    broadcaster_thread.start()

    # Start listening thread
    listener_thread = threading.Thread(target=listen_for_devices, args=(my_username, known_devices), daemon=True)
    listener_thread.start()

    # Keep the main thread alive and allow user to send voice
    try:
        while True:
            time.sleep(1)
            if known_devices:
                print("\nDiscovered devices:")
                for i, (ip, username) in enumerate(known_devices.items(), start=1):
                    print(f"{i}. {ip} - {username}")

                target_input = input("Enter target IP addresses to send voice (comma-separated, or 'exit' to quit): ")
                if target_input.lower() == 'exit':
                    break

                # Split the input by commas and remove any whitespace
                target_ips = [ip.strip() for ip in target_input.split(',') if ip.strip() in known_devices]
                if target_ips:
                    send_voice(target_ips)
                else:
                    print("No valid IP addresses selected.")
    except KeyboardInterrupt:
        print("Exiting device discovery.")
