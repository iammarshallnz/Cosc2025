import sys
import time
import socket

import select
def loadConfig(file : str) -> tuple: # does all loading and checking of config
    try:
        #print(file)
        config : list = open(file[0]).readlines() # open file and read lines to list
        
        routerId : int = int( config[0].split()[1]) #takes config [0]
        inputPorts : list[int] = [int(x.strip(',')) for x in config[1].split()[1:]] #takes config [1 ] splits fopr each into list
        neighboorInfo : list[tuple[int, int, int]] = [tuple(int(i) for i in x.strip(',').split('-')) for x in config[2].split()[1:]] #takes config [2] splits for each in list
        # neighboorInfo (input port , link cost , routerId)
        return routerId, inputPorts, neighboorInfo #returns each in 3 tuple
    except:
        print("Error in config file")

def receiver(any_socket: socket.SocketType) -> tuple:

    # gets date and address
    try:
        message, ret_ip = any_socket.recvfrom(1024)

        # ret_ip is tuple (ip, port)
    except TimeoutError:
        print("ERROR: Receiving timed out, dropping packet")
        return None
    except Exception as e:
        print(f"ERROR: Receiving failed: {e}, dropping packet")
        return None
    return (message, ret_ip)


def sendPing(originSocket : socket.socket, neighboorInfo : tuple):
    """Sends a ping message to a neighbor."""
    try:
        message = f"Ping from {originSocket.getsockname()} to {neighboorInfo}"
        originSocket.sendto(message.encode(), ('localhost', neighboorInfo[0]))
        print(f"Sent: {message}")
    except Exception as e:
        print(f"ERROR: Failed to send ping: {e}")
def main():
    # main function
    
    ## TODO #1
    argv = sys.argv[1:] # plug in arg later ?? 
    #print(loadConfig(argv))
    routerId, inputPorts, neighboorInfo = loadConfig(argv)
    open_Sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for port in inputPorts] #scalable with config] # holding objects to close later  ???
    readableSockets = []
    
    for port in inputPorts: #scalable with config
        temp = open_Sockets.pop()
        temp.bind(('localhost', port))
        temp.setblocking(False)
        readableSockets.append(temp) # bind each socket 
    sendingSocket : socket.socket = readableSockets[0]   # take one of the sockets as main out going
    lastSendTime = time.time()
    
        
    while 1:
        r, _, _ = select.select(readableSockets, [], [], 1) #BLOCKS TILL TIMEOUT, 0 is polling 
        for readable in r: # enters for when readable is Ready
            
            data = receiver(readable)
            if data:
                data, addr = data
                print(f'\nhello {addr} : {data.decode()}')
        
            
        # Periodically send pings to neighbors
        currentTime = time.time()
        if currentTime - lastSendTime >= 2:  # Send every 5 seconds
            for neighbor in neighboorInfo:
                sendPing(readableSockets[0], neighbor)  # Use the first socket for sending
            lastSendTime = currentTime

    

main()