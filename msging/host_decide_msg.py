# host.py
import socket
import threading
import sys

# Configuration
BUFFER_SIZE = 1024  # Maximum size of incoming messages

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
    Initiates connection to the client and facilitates messaging upon acceptance.
    """
    client_ip = input("Enter the client's IP address: ").strip()
    client_port = 50010  # Must match the client's listening port

    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host.connect((client_ip, client_port))
        print(f"[CONNECTED] Connected to client at {client_ip}:{client_port}")
    except Exception as e:
        print(f"[ERROR] Could not connect to client: {e}")
        sys.exit()

    try:
        # Wait for the client's response to the connection request
        response = host.recv(BUFFER_SIZE).decode('utf-8')
        if response == "ACCEPT":
            print("[INFO] Connection accepted by the client. You can start chatting.")
        elif response == "REJECT":
            print("[INFO] Connection rejected by the client.")
            host.close()
            sys.exit()
        else:
            print(f"[INFO] Received unexpected response: {response}")
            host.close()
            sys.exit()
    except Exception as e:
        print(f"[ERROR] Failed to receive response from client: {e}")
        host.close()
        sys.exit()

    # Start threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(host,), daemon=True)
    send_thread = threading.Thread(target=send_messages, args=(host,), daemon=True)
    receive_thread.start()
    send_thread.start()

    # Wait for threads to finish
    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":
    start_host()
