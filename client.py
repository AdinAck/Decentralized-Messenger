import threading
import socket

class User:
    def __init__(self, id='', addr='', name=''):
        if id == '':
            self.id = genId()
        self.addr = addr
        self.name = name
        self.status = False

class Client:
    def __init__(self, sckt, chats, contacts):
        self.s = sckt
        self.chatDict = {chat.id: chat for chat in chats}
        self.contacts = contacts
        self.s.settimeout(socket.getdefaulttimeout())

        threading.Thread(target=self.mainloop, daemon=True).start()

    def mainloop(self):
        while self.run:
            command = int.from_bytes(self.s.recv(1), "little")
            header = int.from_bytes(self.s.recv(1), "little")
            data = self.s.recv(header).decode()

            if command == 0: # A new user is in the group
                stuff = data.split(",") # id, addr, name
                self.contacts[stuff[0]] = User(id=stuff[0], addr=stuff[1], name=stuff[2])
                self.contacts[stuff[0]].status = True

            elif command == 1: # A user has sent a message
                stuff = data.split(",") # group ID, timestamp, user ID, message
                self.chatDict[stuff[0]].history[stuff[1]] = (stuff[2], stuff[3])

            elif command == 2: # A user has disconnected
                self.contacts[data].status = False
