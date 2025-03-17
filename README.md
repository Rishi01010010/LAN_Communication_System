# 🖧 LAN Communication System: Secure Local Networking 🖧

Welcome to the *LAN Communication System*, a robust project developed by students at SAI Vidya Institute of Technology, Bengaluru, under the guidance of Dr. Tejashwini N. This system enables secure, real-time text messaging and voice communication within a Local Area Network (LAN), designed to operate independently of paid internet services. Built using Python with Flask and Socket.IO, it’s an innovative solution for organizations and communities seeking efficient connectivity.

## 🔍 Project Overview

The *LAN Communication System* addresses the growing need for secure, cost-effective communication in an era of digital vulnerabilities. By leveraging TCP for reliable text messaging and UDP for low-latency voice calls, the system facilitates resource sharing and collaboration within a limited area (e.g., home, office, or campus). This project, presented as part of a Computer Networks course, showcases a blend of practical implementation and theoretical research.

### ✨ Key Features:

- *Real-Time Text Messaging:* Uses TCP and Socket.IO for reliable message delivery.
- *Voice Communication:* Implements UDP-based audio streaming with PyAudio for seamless calls.
- *User-Friendly Interface:* Web-based UI built with HTML and JavaScript.
- *Device Discovery:* Automatically detects and connects devices on the LAN.
- *Independent Operation:* Functions without external internet reliance.

## 🚀 Getting Started

### 1. *Prerequisites:*
- Python 3.x installed on your system.
- Required libraries: Flask, Flask-SocketIO, PyAudio, and basic networking tools.
- A LAN setup with at least two devices (e.g., computers, laptops, or smartphones).

### 2. *Setting Up:*

- Clone the repository (if hosted on GitHub):
  ```bash
  git clone https://github.com/your-username/LAN_Communication_System.git
  cd LAN_Communication_System
  ```

- Install dependencies:
  ```bash
  pip install flask flask-socketio pyaudio
  ```

- Prepare your LAN environment:
  - Ensure devices are connected via a router, switch, or Wi-Fi access point.
  - Assign static IP addresses if needed (e.g., 192.168.1.x).

- Extract ZIP files (optional):
  - Unzip `Broadcaster.zip`, `calling.zip`, `msging.zip`, and `voice_communication/final.zip` from the `New folder/` to access additional scripts.

### 3. *Running the System:*

- **Text Messaging:**
  - Navigate to `msging/final/`.
  - Run the host script:
    ```bash
    python adv_msg_hosting.py
    ```
  - Run the client script on another device:
    ```bash
    python client_decide_msg.py
    ```
  - Open a web browser and connect to the host’s IP (e.g., `http://192.168.1.10:5000`) to register and chat.

- **Voice Communication:**
  - Navigate to `voice_communication/`.
  - Start the sender on one device:
    ```bash
    python send.py
    ```
  - Start the receiver on another device:
    ```bash
    python receive.py
    ```
  - Use `last_send.py` and `last_receive.py` in `voice_communication/final/` for the final version.

- **Broadcaster:**
  - Navigate to `Broadcaster/`.
  - Run `send.py` to broadcast messages and `receive.py` to listen.

- **Calling:**
  - Navigate to `calling/`.
  - Run `host.py` on the host device and `client.py` on the client device to initiate calls.

### 4. *Sample Output:*
- **Chat Interface:**
  ```
  Register
  Windows 192.168.1.10
  Chat
  Android
  Enter Message: Hello Windows
  Messages: Message from Android: Hello Windows
  ```

## 💾 Directory Structure

```
LAN_Communication_System/
│
├── README.md                  # Project documentation
│
├── Broadcaster/               # Scripts for broadcasting messages
│   ├── receive.py             # Receives broadcasted messages
│   └── send.py                # Sends broadcasted messages
│
├── calling/                   # Scripts for call initiation
│   ├── client.py              # Client-side call script
│   └── host.py                # Host-side call script
│
├── msging/                    # Text messaging module
│   ├── host_decide_msg.py     # Initial host script
│   └── final/                 # Final messaging implementation
│       ├── adv_msg_hosting.py  # Advanced host script
│       ├── client_decide_msg.py # Client script
│       └── device_discovery.py # Device discovery module
│
├── New folder/                # Archived files
│   ├── Broadcaster.zip        # Compressed Broadcaster folder
│   ├── calling.zip            # Compressed calling folder
│   └── msging.zip             # Compressed msging folder
│
└── voice_communication/       # Voice communication module
    ├── final.zip              # Compressed final voice scripts
    ├── receive.py             # Receives audio data
    ├── Receiver.py            # Alternative receiver script
    ├── send.py                # Sends audio data
    ├── Sender.py              # Alternative sender script
    ├── tempCodeRunnerFile.py   # Temporary runner file
    └── final/                 # Final voice implementation
        ├── last_receive.py     # Final receiver script
        └── last_send.py        # Final sender script
```

### 📝 Code Explanation

1. **msging/final/adv_msg_hosting.py**:
   - Hosts a Flask server with Socket.IO for real-time text messaging.
   - Manages user registration and message routing using TCP sockets.

2. **voice_communication/send.py**:
   - Captures audio input with PyAudio and streams it via UDP sockets.
   - Implements low-latency voice communication.

3. **Broadcaster/send.py**:
   - Broadcasts messages across the LAN for testing connectivity.

4. **calling/host.py**:
   - Establishes a call session and signals the client for voice communication.

## 🌐 System Architecture

- **User Registration:** Users provide a username and IP address, stored for communication.
- **Socket Connection:** TCP for text messaging, UDP for voice streaming.
- **Text Messaging:** Processed and delivered via Socket.IO rooms.
- **Voice Calls:** Initiated with a signal, followed by UDP-based audio streaming.
- **Real-Time Interaction:** Ensures seamless communication without delays.

## 🛠️ How It Works

1. *Text Messaging:*
   - Users register via a web interface.
   - Messages are sent over TCP sockets and routed by the Flask server.
   - Recipients receive messages in real-time.

2. *Voice Communication:*
   - A call is initiated with a signal via TCP.
   - Audio is captured, streamed over UDP, and played back on the receiver.

3. *Device Discovery:*
   - Automatically detects devices on the LAN for easy connection.

## 🎯 Project Intent

The *LAN Communication System* aims to provide a secure, cost-effective communication solution for local networks. It serves as a foundation for future enhancements like video calls and scalability, making it valuable for educational projects, small organizations, and research in network security.

## 🔧 Customization

Enhance the project with these ideas:
- *Add Video Calls:* Integrate OpenCV for video streaming over UDP.
- *Improve UI:* Develop a more interactive interface with CSS frameworks like Bootstrap.
- *Scalability:* Optimize for larger networks with load balancing.
- *Security:* Add encryption (e.g., TLS) for text and voice data.

## 📌 References
- Ghini, V., et al. (2023). *Always Best Packet Switching: The Mobile VoIP Case Study*. International Journal of Network Management.
- Sinam, T., et al. (2022). *A Technique for Classification of VoIP Flows*. IEEE Transactions on Multimedia.
- Zhang, X., & Schulzrinne, H. (2004). *Voice over TCP and UDP*. Journal of Computer Networks.
- Abba, I. M., et al. (2023). *LAN CHAT MESSENGER (LCM) USING JAVA PROGRAMMING WITH VOIP*. Journal of Software Engineering.
