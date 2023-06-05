import socket
import threading

UDP_MAX_SIZE = 65535
TCP_MAX_SIZE = 1024

udpPort = 55555
tcpPort = 3000

closeString = "__closeX55502331"
encodingString = "utf-8"

# UDP
class ConnectUDP():

    def __init__(self, callback):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.callback = callback

    def listen(self, sock: socket.socket):
        while True:
            try:
                msg, addr = sock.recvfrom(UDP_MAX_SIZE)
                decoded_msg = msg.decode(encodingString)
                self.callback(decoded_msg)
            except socket.error as e:
                print("An error occurred!")
                self.sock.close()
                break


    def connect(self, host: str = '127.0.0.1', port: int = udpPort, nickName: str = "Noname"):
        self.sock.connect((host, port))

        threading.Thread(target=self.listen, args=(self.sock,), daemon=True).start()

        self.sock.send(f'__join:{nickName}'.encode(encodingString))

    def send(self, message):
        self.sock.send(message.encode(encodingString))

    def close(self):
        self.sock.send(closeString.encode(encodingString))
        self.sock.close()


# TCP
class ConnectTCP():

    nickname = "No name"

    def __init__(self, callback):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.callback = callback

    def listen(self):
        while True:
            try:
                message = self.sock.recv(TCP_MAX_SIZE)
                decodedMessage = message.decode(encodingString)
                if decodedMessage == "NICK":
                    self.sock.send(self.nickname.encode(encodingString))
                else:
                    self.callback(decodedMessage)
            except:
                print("An error occurred!")
                self.sock.close()
                break


    def connect(self, host: str = '127.0.0.1', port: int = tcpPort, nickName: str = "Noname"):
        self.sock.connect((host, port))

        threading.Thread(target=self.listen).start()

        self.nickname = nickName

        # self.sock.send(f'__join:{nickName}'.encode(self.encodingString))

    def send(self, message):
        self.sock.send(message.encode(encodingString))

    def close(self):
        self.sock.send(closeString.encode(encodingString))
        self.sock.close()