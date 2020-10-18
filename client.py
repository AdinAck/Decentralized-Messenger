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
    def __init__(self, user, sckt, chat, contacts):
        self.user = user
        self.s = sckt
        self.chat = chat
        self.contacts = contacts
        self.s.settimeout(socket.getdefaulttimeout())
        self.run = True

        # threading.Thread(target=self.mainloop, daemon=True).start()

    def mainloop(self):
        msg = f'{self.user.id},{self.user.name}'
        self.s.send(bytearray([1, len(msg)]))
        self.s.send(msg.encode())

        while self.run:
            command = int.from_bytes(self.s.recv(1), "little")
            header = int.from_bytes(self.s.recv(1), "little")
            data = self.s.recv(header).decode()

            if command == 1: # A new user is in the group
                stuff = data.split(",") # id, addr, name
                if stuff[1] == 'HOST':
                    stuff[1] = self.s.getpeername()[0]
                self.contacts[stuff[0]] = User(id=stuff[0], addr=stuff[1], name=stuff[2])
                self.chat.members.append(self.contacts[stuff[0]])
                self.contacts[stuff[0]].status = True
                print(f'{stuff[2]} now exists.')

            elif command == 2: # A user has sent a message
                stuff = data.split(",") # group ID, timestamp, user ID, message
                self.chat.history[stuff[1]] = (stuff[2], stuff[3])
                print(f'{self.contacts[stuff[2]].name}: {stuff[3]}')

            elif command == 3: # A user has disconnected
                self.contacts[data].status = False
