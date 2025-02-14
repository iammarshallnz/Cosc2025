import sys

import socket as socket

def loadConfig(file : str) -> tuple: # does all loading and checking of config
    try:
        config : list = open('COSC364/ass1/config.txt').readlines()
        routerId : int = int( config[0].split()[1])
        inputPorts : list[int] = [int(x.strip(',')) for x in config[1].split()[1:]]
        neighboorInfo : list[tuple[int, int, int]] = [tuple(int(i) for i in x.strip(',').split('-')) for x in config[2].split()[1:]]
        #(input port , link cost , routerId)
        return routerId, inputPorts, neighboorInfo
    except:
        print("Error in config file")


def main():
    # main function
    
    ## TODO #1
    argv = sys.argv[1:] # plug in arg later ?? 
    print(loadConfig(argv))
    routerId, inputPorts, neighboorInfo = loadConfig(argv)
    inputSockets = []
    
    for port in inputPorts:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as tempSocket:
            
            tempSocket.bind(('localhost', port))
            
            print(tempSocket)
            inputSockets.append(tempSocket)
    
    while 1:
        for i in inputSockets:
            print(i)
            i.listen()
 
    # must close socket
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print("ERROR: Socket creation failed")
        sys.exit()

    # simplify variables
    
    message =  None #dt_resquest(dt)

    addr = ('localhost', port)
    try:
        clientSocket.sendto(message, addr)
        
      

    except:
        
        print("ERROR: Sending failed")
        clientSocket.close()
        sys.exit()

    clientSocket.settimeout(1)

    
    
    clientSocket.close()
    sys.exit()
    

main()