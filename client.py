import threading
import socket
from time import sleep

class User:
    def __init__(self, id='', addr='', name=''):
        if id == '':
            self.id = genId()
        else:
            self.id = id
        self.addr = addr
        self.name = name
        self.status = False

class Client:
    def __init__(self, network, user, sckt, chat, contacts, h):
        self.user = user
        self.s = sckt
        self.chat = chat
        self.contacts = contacts
        self.network = network
        self.h = h
        self.s.settimeout(socket.getdefaulttimeout())
        self.run = True

        # threading.Thread(target=self.mainloop, daemon=True).start()

    def mainloop(self):
        msg = f'{self.chat.id},{self.user.id},{self.user.name}'
        self.s.send(bytearray([1, len(msg)]))
        self.s.send(msg.encode())
        self.chat.members[self.user.id] = self.user

        while self.run:
            try:
                command = int.from_bytes(self.s.recv(1), "little")
                header = int.from_bytes(self.s.recv(1), "little")
                data = self.s.recv(header).decode()

                if command == 1: # A new user is in the group
                    stuff = data.split(",") # id, addr, name
                    if stuff[1] != 'HOST':
                        stuff = stuff[0], stuff[1][2:-1], stuff[3]
                    else:
                        stuff[1] = self.s.getpeername()[0]
                        self.hostUserID = stuff[0]
                        self.network.connections.append(stuff[0])
                    self.contacts[stuff[0]] = User(id=stuff[0], addr=stuff[1], name=stuff[2])
                    self.chat.members[stuff[0]] = self.contacts[stuff[0]]
                    self.contacts[stuff[0]].status = True
                    self.chat.messages += f"\n{self.contacts[stuff[0]].name} has come online."
                    print(f'{stuff[2]} now exists.')

                elif command == 2: # A user has sent a message
                    stuff = data.split(",") # group ID, timestamp, user ID, message
                    self.chat.history[int(stuff[1])] = (stuff[2], stuff[3])
                    if stuff[0] == self.chat.id:
                        self.chat.messages += f'\n{self.contacts[stuff[2]].name}: {stuff[3]}'
                        print(f'{stuff[0]},{self.contacts[stuff[2]].name}: {stuff[3]}')

                elif command == 3: # A user has disconnected
                    self.contacts[data].status = False
                    self.chat.messages += f"\n{self.contacts[data].name} has gone offline."

                elif command == 4:
                    self.chat.name = data
                    self.h.chatgfx[-1].configure(text=data)
                    self.h.gNameText.set(data)
                    print(f'Chat is named {data}')

            except ConnectionResetError:
                print(f"Host for {self.chat.id} disconnected, closing...")
                print(self.network.connections)
                print(self.hostUserID)
                self.network.connections.remove(self.hostUserID)
                sortedUsers = sorted([key for key in self.chat.members if key != self.hostUserID])
                print(sortedUsers)
                for userID in sortedUsers:
                    print(userID)
                    if self.user.id == userID:
                        print("Hosting")
                        self.network.hostList.append(self.chat)
                        return
                    else:
                        print("Looking for host")
                        sleep(2)
                        if self.network.findHost(self.chat):
                            return
                        else:
                            self.network.hostList.remove(self.chat)
                            continue
                self.network.findHost(self.chat)
                return
