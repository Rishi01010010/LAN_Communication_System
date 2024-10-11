
import socket
import pyaudio

# Configuration
TARGET_IP = input("Enter target IP address: ")
UDP_PORT = 50020
BUFFER_SIZE = 1024  # Size of outgoing audio chunks

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

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
    send_voice(TARGET_IP)