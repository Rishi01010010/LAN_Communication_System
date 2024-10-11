import socket
import pyaudio

# Configuration
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 50020
BUFFER_SIZE = 4096  # Size of incoming audio chunks

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def receive_voice():
    """Receives audio data over UDP and plays it through the speakers."""
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
    print("Starting voice receiver...")
    receive_voice()
