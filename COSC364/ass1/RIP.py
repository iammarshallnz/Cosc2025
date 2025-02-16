import sys
import time
import socket
import select
from typing import List, Tuple, Optional

# Constants
LOCALHOST = 'localhost'
BUFFER_SIZE = 1024
PING_INTERVAL = 2  # seconds
DEFAULT_TIMEOUT = 1  # second

class ConfigError(Exception):
    """Custom exception for configuration file errors."""
    pass

def parse_router_id(line: str) -> int:
    """Extract and validate router ID from config line."""
    try:
        return int(line.split()[1])
    except (IndexError, ValueError):
        raise ConfigError("Invalid router ID format")

def parse_input_ports(line: str) -> List[int]:
    """Extract and validate input ports from config line."""
    try:
        return [int(x.strip(',')) for x in line.split()[1:]]
    except ValueError:
        raise ConfigError("Invalid input ports format")

def parse_neighbor_info(line: str) -> List[Tuple[int, int, int]]:
    """Extract and validate neighbor information from config line.
    Returns list of tuples: (input_port, link_cost, router_id)
    """
    try:
        return [tuple(int(i) for i in x.strip(',').split('-')) 
                for x in line.split()[1:]]
    except ValueError:
        raise ConfigError("Invalid neighbor info format")

def load_config(config_file: str) -> Tuple[int, List[int], List[Tuple[int, int, int]]]:
    """Load and validate router configuration from file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Tuple containing:
        - router_id: Unique identifier for this router
        - input_ports: List of ports this router listens on
        - neighbor_info: List of (port, cost, router_id) for neighbors
        
    Raises:
        ConfigError: If configuration is invalid
    """
    try:
        with open(config_file) as f:
            lines = f.readlines()
            
        if len(lines) < 3:
            raise ConfigError("Configuration file must have at least 3 lines")
            
        router_id = parse_router_id(lines[0])
        input_ports = parse_input_ports(lines[1])
        neighbor_info = parse_neighbor_info(lines[2])
        
        return router_id, input_ports, neighbor_info
    
    except (IOError, IndexError) as e:
        raise ConfigError(f"Error reading config file: {e}")

def setup_sockets(input_ports: List[int]) -> List[socket.socket]:
    """Create and bind UDP sockets for all input ports.
    
    Args:
        input_ports: List of ports to listen on
        
    Returns:
        List of configured socket objects
    """
    sockets = []
    for port in input_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LOCALHOST, port))
        sock.setblocking(False)
        sockets.append(sock)
    return sockets

def receive_message(sock: socket.socket) -> Optional[Tuple[bytes, Tuple]]:
    """Receive and validate incoming message from socket.
    
    Returns:
        Tuple of (message, address) if successful, None if error
    """
    try:
        message, address = sock.recvfrom(BUFFER_SIZE)
        return message, address
    except (TimeoutError, BlockingIOError):
        return None
    except Exception as e:
        print(f"ERROR: Receiving failed: {e}")
        return None

def send_ping(sock: socket.socket, neighbor: Tuple[int, int, int]) -> None:
    """Send ping message to neighbor router.
    
    Args:
        sock: Socket to send from
        neighbor: Tuple of (port, cost, router_id)
    """
    try:
        message = f"Ping from {sock.getsockname()} to {neighbor}"
        sock.sendto(message.encode(), (LOCALHOST, neighbor[0]))
        print(f"Sent: {message}")
    except Exception as e:
        print(f"ERROR: Failed to send ping: {e}")

def main():
    try:
        config_file = sys.argv[1]
        config = RouterConfig(config_file)
        router = Router(config)
        router.run()
    except (ConfigError, IndexError) as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()