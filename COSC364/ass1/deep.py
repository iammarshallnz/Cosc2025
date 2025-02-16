import sys
import socket
import select
import time

def loadConfig(file: str) -> tuple:
    """Loads and validates the configuration file."""
    try:
        with open(file, 'r') as f:
            config = f.readlines()

        # Extract router ID
        routerId = int(config[0].split()[1])

        # Extract input ports
        inputPorts = [int(x.strip(',')) for x in config[1].split()[1:]]

        # Extract neighbor information (input port, link cost, routerId)
        neighborInfo = [tuple(int(i) for i in x.strip(',').split('-')) for x in config[2].split()[1:]]

        return routerId, inputPorts, neighborInfo
    except Exception as e:
        print(f"Error in config file: {e}")
        sys.exit(1)

def receiver(any_socket: socket.socket) -> tuple:
    """Receives data from a socket."""
    try:
        message, ret_ip = any_socket.recvfrom(1024)
        return message, ret_ip
    except TimeoutError:
        print("ERROR: Receiving timed out, dropping packet")
        return None
    except Exception as e:
        print(f"ERROR: Receiving failed: {e}, dropping packet")
        return None

def sendPing(originSocket: socket.socket, neighborInfo: tuple):
    """Sends a ping message to a neighbor."""
    try:
        message = f"Ping from {originSocket.getsockname()} to {neighborInfo}"
        originSocket.sendto(message.encode(), ('localhost', neighborInfo[0]))
        print(f"Sent: {message}")
    except Exception as e:
        print(f"ERROR: Failed to send ping: {e}")

def main():
    # Load configuration
    if len(sys.argv) < 2:
        print("Usage: python script.py <config_file>")
        sys.exit(1)

    routerId, inputPorts, neighborInfo = loadConfig(sys.argv[1])

    # Create and bind sockets
    openSockets = []
    for port in inputPorts:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('localhost', port))
        sock.setblocking(False)
        openSockets.append(sock)

    print(f"Router ID: {routerId}")
    print(f"Listening on ports: {inputPorts}")
    print(f"Neighbors: {neighborInfo}")

    # Main loop
    lastSendTime = time.time()
    while True:
        # Check for incoming messages
        readable, _, _ = select.select(openSockets, [], [], 1)  # Timeout of 1 second

        for sock in readable:
            data = receiver(sock)
            if data:
                message, addr = data
                print(f"Received from {addr}: {message.decode()}")

        # Periodically send pings to neighbors
        currentTime = time.time()
        if currentTime - lastSendTime >= 5:  # Send every 5 seconds
            for neighbor in neighborInfo:
                sendPing(openSockets[0], neighbor)  # Use the first socket for sending
            lastSendTime = currentTime

if __name__ == "__main__":
    main()