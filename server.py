import threading
import socket

class User:
    def __init__(self, sock, addr, name="UNKNOWN"):
        self.sock, self.addr, self.name = sock, addr, name

class Server:
    def __init__(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', port))
        self.s.listen()

        self.users = []

        while True:
            clientsocket, address = self.s.accept()
            print(f"[INFO] Connection from {address} has been established.")
            self.users.append(user(clientsocket, address))
            threading.Thread(target=self.client, args=[self.users[-1]]).start()

    def initialize(self, user, data):
        if user.name == "UNKNOWN":
            stuff = data.split(",")
            # if stuff[0] in [i.name for i in self.users]:
            #     print(f"[WARN] {user.addr} username already taken.")
            #     user.sock.send(bytearray([6]))
            #     continue
            user.name = stuff[0]
            user.color = int(stuff[1]),int(stuff[2]),int(stuff[3])
            print(f"[INFO] {user.addr} initialized. Name is {user.name}, color is {user.color}")
            for p in [i for i in self.users if i != user]:
                msg = p.name+","+str(p.color[0])+","+str(p.color[1])+","+str(p.color[2])
                user.sock.send(bytearray([1, len(msg)]))
                user.sock.send(msg.encode())
                # print(f"told {user.name} that {p.name} exists")
                msg = user.name+","+str(user.color[0])+","+str(user.color[1])+","+str(user.color[2])
                p.sock.send(bytearray([1, len(msg)]))
                p.sock.send(msg.encode())
                # print(f"told {p.name} that {user.name} exists")

    def client(self, user):
        while True:
            try:
                command = int.from_bytes(user.sock.recv(1), "little")
                if command == 0:
                    threading.Thread(target=self.sendCoords, args=[user]).start()
                    continue
                header = int.from_bytes(user.sock.recv(1), "little")
                data = user.sock.recv(header).decode()
                if command == 4:
                    threading.Thread(target=self.initialize, args=[user, data]).start()
                elif command == 2: # user sends coordinates
                    threading.Thread(target=self.recvCoords, args=[user, data]).start()
            except ConnectionResetError:
                threading.Thread(target=self.inform, args=[user]).start()
                return
            except IndexError:
                print(f"[WARN] Received bad packets from {user.name}.")
            except Exception as e:
                print(f"[ERR] [{user.addr}] {e}")
                self.users.remove(user)
                return

    def inform(self, user):
        try:
            self.users.remove(user)
            print(f"[INFO] {user.name} has left.")
            user.sock.close()
            for p in [i for i in self.users if i != user]:
                try:
                    p.sock.send(bytearray([3, len(user.name)]))
                    p.sock.send(user.name.encode())
                except ConnectionResetError:
                    self.inform(p)
        except ValueError:
            return

if __name__ == "__main__":
    Server(80)
