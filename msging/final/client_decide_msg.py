# client.py
import socket
import threading
import sys

# Configuration
CLIENT_HOST = ''  # Listen on all available interfaces
CLIENT_PORT = 50010
BUFFER_SIZE = 1024  # Maximum size of incoming messages

def handle_client_connection(client_socket, addr):
    """
    Handles the incoming connection request from the host.
    Prompts the user to accept or reject the connection.
    """
    print(f"[REQUEST] Connection request from {addr}")

    while True:
        decision = input(f"Do you want to accept the connection from {addr}? (yes/no): ").strip().lower()
        if decision in ['yes', 'no']:
            break
        else:
            print("Please enter 'yes' or 'no'.")

    if decision == 'yes':
        try:
            client_socket.sendall("ACCEPT".encode('utf-8'))
            print(f"[ACCEPTED] Connection accepted with {addr}")
        except Exception as e:
            print(f"[ERROR] Failed to send acceptance: {e}")
            client_socket.close()
            return

        # Start threads for sending and receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
        send_thread = threading.Thread(target=send_messages, args=(client_socket,), daemon=True)
        receive_thread.start()
        send_thread.start()

        # Wait for threads to finish
        receive_thread.join()
        send_thread.join()
    else:
        try:
            client_socket.sendall("REJECT".encode('utf-8'))
            print(f"[REJECTED] Connection rejected with {addr}")
        except Exception as e:
            print(f"[ERROR] Failed to send rejection: {e}")
        client_socket.close()

def receive_messages(sock):
    """
    Listens for incoming messages from the host and prints them.
    """
    while True:
        try:
            message = sock.recv(BUFFER_SIZE).decode('utf-8')
            if not message:
                # Host has closed the connection
                print("[INFO] Host disconnected.")
                break
            print(f"Host: {message}")
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
    Sends messages to the host.
    """
    try:
        while True:
            message = input()
            if message.lower() == 'exit':
                print("[INFO] Disconnecting from host.")
                break
            if message.strip() == '':
                continue  # Ignore empty messages
            sock.sendall(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("\n[INFO] Keyboard interrupt received. Disconnecting.")
    finally:
        sock.close()
        print("[INFO] Disconnected from host.")
        sys.exit()

def start_client():
    """
    Starts the client server to listen for incoming connections.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((CLIENT_HOST, CLIENT_PORT))
    server.listen(5)
    print(f"[LISTENING] Client listening on port {CLIENT_PORT}...")

    try:
        while True:
            client_socket, addr = server.accept()
            client_handler = threading.Thread(target=handle_client_connection, args=(client_socket, addr), daemon=True)
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Shutting down the client.")
    finally:
        server.close()
        sys.exit()

if __name__ == "__main__":
    start_client()
