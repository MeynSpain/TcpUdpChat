import socket
import threading

UDP_MAX_SIZE = 65535
TCP_MAX_SIZE = 1024

closeString = "__closeX55502331"
encodingString = "utf-8"

host = input("Input ip host:")

# host = '127.0.0.1'

tcpPort = 3000
udpPort = 55555

# TCP connection
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.bind((host, tcpPort))
tcpServer.listen()

# UDP connection
udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServer.bind((host, udpPort))

clientsTCP = []
clientsUDP = []
nickNames = {}

tcpPorts = []


def handleTCP(client):
    while True:
        try:
            message = client.recv(TCP_MAX_SIZE)
            decodedMessage = message.decode(encodingString)

            if decodedMessage == closeString:
                msg = f"Client {nickNames[client.getpeername()]} left from chat!"
                print(msg)

                clientsTCP.remove(client)
                nickNames.pop(client.getpeername())

                broadcastUDP(msg, None)
                broadcastTCP(msg, client)
                client.close()
                break
            else:
                broadcastTCP(decodedMessage, client)
                broadcastUDP(decodedMessage, None)

            # print(f"UDP client {address} connect to server:")

        except ConnectionResetError:
            # index = clientsTCP.index(client)
            # clientsTCP.remove(client)
            # client.close()

            nickName = nickNames.get(client.getpeername())
            nickNames.pop(client.getpeername())

            clientsTCP.remove(client)
            client.close()


            broadcastTCP(f'{nickName} left from chat!', client)
            broadcastUDP(f'{nickName} left from chat!', None)


            break

# def handleUDP():
#     message, address = udpServer.recv(UDP_MAX_SIZE)
#     broadcast(message, None)

def receiveTCP():
    while True:
        client, address = tcpServer.accept()
        print(f"TCP client connected from {address}")

        # tcpPorts.append(address)

        client.send('NICK'.encode(encodingString))
        nickName = client.recv(TCP_MAX_SIZE).decode(encodingString)
        nickNames[address] = nickName
        clientsTCP.append(client)

        print(f"Nickname of the TCP client: {nickName}")
        broadcastTCP(f'{nickName} joined the chat!', client)
        broadcastUDP(f'{nickName} joined the chat!', None)
        client.send('Connected to server'.encode('utf-8'))

        thread = threading.Thread(target=handleTCP, args=(client,))
        thread.start()

def receiveUDP():
    while True:
        message, address = udpServer.recvfrom(UDP_MAX_SIZE)

        if not message:
            continue

        if address not in clientsUDP:
            clientsUDP.append(address)

        decodedMessage = message.decode(encodingString)



        if '__join' in decodedMessage:
            nickname = decodedMessage.split(':', 1)[1]

            print(f"Client {nickname} joined chat")
            nickNames[address] = nickname
            msg = f"Client {nickname} joined to chat!"
            broadcastUDP(msg, address)
            broadcastTCP(msg, None)
            continue

        nickname = nickNames.get(address)

        if decodedMessage == closeString:
            # nickname = nickNames.get(address)

            msg = f"Client {nickname} left from chat!"
            print(msg)

            clientsUDP.remove(address)
            nickNames.pop(address)

            broadcastUDP(msg, address)
            broadcastTCP(msg, None)
        else:
            # msg = f"{nickname}:{decodedMessage}"
            broadcastUDP(decodedMessage, address)
            broadcastTCP(decodedMessage, None)



def broadcastTCP(message, senderSocket):
    for clientSocket in clientsTCP:
        if clientSocket != senderSocket:
            clientSocket.send(message.encode(encodingString))

def broadcastUDP(message, senderAddress):
    for client in clientsUDP:
        if client == senderAddress:
            continue
        udpServer.sendto(message.encode(encodingString), client)


print("Server is listening...")

tcp_receive_thread = threading.Thread(target=receiveTCP)
tcp_receive_thread.start()

udp_receive_thread = threading.Thread(target=receiveUDP)
udp_receive_thread.start()