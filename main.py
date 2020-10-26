import threading
import socket
from server import Server
from client import Client
from tkinter import *
from tkinter import ttk
from functools import partial
import pickle
import random
from datetime import datetime
import time

class User:
    def __init__(self, id='', addr='', name=''):
        if id == '':
            self.id = genId()
        else:
            self.id = id
        self.addr = addr
        self.name = name
        self.status = False

class Chat:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.members = {}
        self.history = {}
        self.text = StringVar()

    @property
    def messages(self):
        return self.text.get()

    @messages.setter
    def messages(self, val):
        self.text.set(val)

class Network:
    def __init__(self, home):
        pass

    def start(self):
        global user, chats, contacts

        self.hostList = []
        threads = []
        self.connections = []
        self.clients = {}

        for chat in chats:
            threads.append(threading.Thread(target=lambda: self.findHost(chat)))
            threads[-1].start()

        for thread in threads:
            thread.join()

        threading.Thread(target=lambda: self.startServer(user, chats, contacts)).start()

    def findHost(self, chat):
        global contacts, user, h
        if len(chat.members) != 0:
            for id, member in chat.members.items():
                if id != user.id:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.1)
                    if id not in self.connections:
                        try:
                            s.connect((member.addr, 8082))
                            self.clients[chat.id] = Client(self, user, s, chat, contacts, h)
                            print(f"Connecting to {chat.id}.")
                            threading.Thread(target=self.clients[chat.id].mainloop, daemon=True).start()
                            self.connections.append(id)
                            return True
                        except socket.timeout:
                            pass

        print(f'{chat.id} has no hosts, adding to host list.')
        self.hostList.append(chat)
        return False

    def startServer(self, user, chats, contacts):
        self.server = Server(user, chats, contacts)

    def clientSend(self, id, command, msg):
        self.clients[id].s.send(bytearray([command, len(msg)]))
        self.clients[id].s.send(msg.encode())

class MenuBar:
    def __init__(self, root):
        self.root = root

    def render(self):
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        profile = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Profile', menu=profile)
        profile.add_command(label='Change Name', command=lambda: swapScreens(n))
        rooms = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Rooms', menu=rooms)
        rooms.add_command(label='Create Room', command=lambda: swapScreens(c))
        rooms.add_command(label='Join Room', command=lambda: swapScreens(j))

class Home:
    def __init__(self, root):
        global chats
        self.root = root
        self.chatgfx = []
        if len(chats) > 0:
            self.viewedChat = chats[0]
        else:
            self.viewedChat = None
    def render(self):
        global currentScreen, chats, net
        currentScreen.append(self)

        self.main = Frame(self.root)
        self.main.pack(fill=BOTH, expand=True)

        leftSideBar = Frame(self.main, bg='#101010')
        leftSideBar.grid(row=0,column=0,sticky='NESW')

        canvas = Canvas(leftSideBar, bg='#101010', bd=0, highlightthickness=0, relief='ridge')
        canvas.pack(side=LEFT, fill=BOTH)

        scrollbar = ttk.Scrollbar(leftSideBar, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set, width=247)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox('all')))

        container = Frame(canvas, width=250, bg='#101010')

        canvas.create_window((0,0), window=container, anchor='sw')

        for i in range(len(chats)):
            self.chatgfx.append(Button(container, text=f'{chats[i].name}', bg='#101010', fg='white',
                                       borderwidth=1, width=34, height=5, anchor='w', justify=LEFT,
                                       highlightbackground='white', command=partial(self.changeChatFocus, chats[i])))
            self.chatgfx[-1].pack(side=TOP)

        rightSideBar = Frame(self.main, width=250, bg='#101010')
        rightSideBar.grid(row=0,column=2,sticky='NESW')

        # self.onlineUsers = Listbox(rightSideBar)
        # self.onlineUsers.pack(side=LEFT, padx=5, pady=5, fill=BOTH)
        #
        # onlineUsersScrollBar = ttk.Scrollbar(rightSideBar, orient=VERTICAL)
        # onlineUsersScrollBar.pack(side=RIGHT, fill=Y)
        #
        # self.onlineUsers.config(yscrollcommand=onlineUsersScrollBar.set)
        # onlineUsersScrollBar.config(command=self.onlineUsers.yview)

        self.main.rowconfigure(0,weight=1)
        self.main.grid_columnconfigure(1,weight=1)

        messageArea = Frame(self.main, bg='#303030')
        messageArea.grid(row=0,column=1,sticky='NESW')

        bottom = Frame(messageArea, bg='#202020')
        bottom.pack(side=BOTTOM, fill=X, expand=False)

        top = Frame(messageArea, bg='#202020')
        top.pack(side=BOTTOM, fill=BOTH, expand=True)

        banner = Frame(messageArea, bg='#202020', height=50)
        banner.pack(side=BOTTOM, fill=X, expand=False)

        self.gNameText = StringVar()

        self.gIDText = StringVar()
        if self.viewedChat != None:
            self.gNameText.set(self.viewedChat.name)
            self.gIDText.set(self.viewedChat.id)

        gNameLabel = Label(banner, textvariable=self.gNameText, fg='white', bg='#202020', font='Roboto 16')
        gNameLabel.pack(side=LEFT, padx=5, pady=5)

        gIDLabel = Entry(banner, state='readonly', textvariable=self.gIDText, readonlybackground='#202020', fg='white',
                         font='Roboto 16', relief='flat')
        gIDLabel.pack(side=LEFT, padx=5, pady=5)

        deleteGroup = Button(banner, text='Delete', bg='#d40f0f', fg='white', borderwidth=0,
                      command=lambda: swapScreens(d))
        deleteGroup.pack(side=RIGHT, padx=5, pady=5)

        self.canvas2 = Canvas(top, bg='#303030', bd=0, highlightthickness=0, relief='ridge')
        self.canvas2.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(top, orient=VERTICAL, command=self.canvas2.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas2.configure(yscrollcommand=scrollbar.set)
        self.canvas2.bind('<Configure>', self.updateCanvas)

        container2 = Frame(self.canvas2, bg='#303030')
        container2.bind('<Configure>', self.updateCanvas)

        self.window = self.canvas2.create_window((0,1000), window=container2, anchor='sw', width=2000, height=2000)

        msgBoxRect = Frame(bottom,height=40, bg='#404040')
        msgBoxRect.pack(side=BOTTOM, fill=X, padx=20,pady=20)

        self.msg = StringVar()

        self.msgBox = Entry(msgBoxRect, bg='#404040', borderwidth=0, font='Roboto 16', fg='#FFFFFF',
                            insertbackground='#909090', textvariable=self.msg)
        msgBoxRect.grid_columnconfigure(0,weight=9)
        msgBoxRect.grid_columnconfigure(1,weight=1)
        self.msgBox.grid(row=0, column=0, sticky='EW', pady=7, padx=5)
        self.msgBox.bind('<Return>', self.handleReturn)

        send = Button(msgBoxRect, text='Send', bg='#0f61d4',fg='white',borderwidth=0,
                      command=lambda: self.sendMsg(self.viewedChat.id, int(datetime.now().strftime("%Y%m%d%H%M%S%f")),
                      self.msgBox.get()))
        send.grid(row=0, column=1, sticky='NSEW')

        self.label = Label(container2, textvariable=StringVar(), bg='#303030', fg='white', font='Roboto 16', anchor='w',
                     justify=LEFT)
        self.label.pack(side=BOTTOM, fill=X, padx=20)
        self.canvas2.itemconfigure(self.window, height=self.label['height'])

    def updateCanvas(self, event):
        self.canvas2.move(self.window, 0, 5)
        self.canvas2.configure(scrollregion = self.canvas2.bbox('all'))

    def changeChatFocus(self, chat):
        print(f"Changed chat to {chat.id}")
        self.viewedChat = chat
        self.label.configure(textvariable=chat.text)
        self.gNameText.set(self.viewedChat.name)
        self.gIDText.set(self.viewedChat.id)
        self.chatgfx[len(chats)-1-chats.index(chat)].configure(text=chat.name)
        # for _, user in self.viewedChat.members.items():
        #     if user.status:
        #         self.onlineUsers.insert(END, user.name)

    def handleReturn(self, event):
        self.sendMsg(self.viewedChat.id, int(datetime.now().strftime("%Y%m%d%H%M%S%f")), self.msgBox.get())
        # self.canvas2.yview_moveto(1)

    def sendMsg(self, gid, time, msg):
        global net, user, chats, h
        if gid not in [chat.id for chat in net.hostList]: # If we are not hosting
            net.clientSend(gid, 2, f'{gid},{time},{msg}')
        else: # If we are hosting
            msg2 = f'{gid},{time},{user.id},{msg}'
            for u in [i for i in net.server.users]:
                u.sock.send(bytearray([2, len(msg2)]))
                u.sock.send(msg2.encode())
        self.msg.set('')
        self.viewedChat.history[int(time)] = user.id, msg
        self.viewedChat.messages += f"\n{user.name}: {msg}"

class JoinRoom:
    def __init__(self, root):
        self.root = root

    def render(self):
        global currentScreen
        currentScreen.append(self)

        self.main = Frame(self.root, bg='#303030')
        self.main.pack(fill=BOTH, expand=True)

        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)
        self.main.grid_columnconfigure(2, weight=1)

        container = Frame(self.main, width=350, height=200, bg='#101010')
        container.grid(row=1, column=1)

        container.grid_propagate(0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1,weight=2)
        container.grid_rowconfigure(2,weight=1)
        container.grid_columnconfigure(0, weight=1)

        title = Label(container, text='Join Room', bg='#101010', fg='white', font='Roboto 16')
        title.grid(row=0, column=0)

        textBoxFrame = Frame(container, bg='#101010')
        textBoxFrame.grid(row=1, column=0, sticky='NEW')

        textBoxFrame.grid_columnconfigure(0, weight=1)
        textBoxFrame.grid_columnconfigure(1, weight=1)
        textBoxFrame.grid_rowconfigure(0, weight=1)
        textBoxFrame.grid_rowconfigure(1, weight=1)

        idLabel = Label(textBoxFrame, text='ID:', bg='#101010', fg='white', font='Roboto 16')
        idLabel.grid(row=0, column=0, ipady=10)

        idEntry = Entry(textBoxFrame, borderwidth=0, bg='#404040', font='Roboto 16', fg='#FFFFFF',
                        insertbackground='#909090')
        idEntry.grid(row=0, column=1)

        ipLabel = Label(textBoxFrame, text='IP:', bg='#101010', fg='white', font='Roboto 16')
        ipLabel.grid(row=1, column=0, ipady=10)

        ipEntry = Entry(textBoxFrame, borderwidth=0, bg='#404040', font='Roboto 16', fg='#FFFFFF',
                        insertbackground='#909090')
        ipEntry.grid(row=1, column=1)

        buttonFrame = Frame(container, bg='#101010')
        buttonFrame.grid(row=2, column=0, sticky='NSEW')

        buttonFrame.grid_columnconfigure(0, weight=10)
        buttonFrame.grid_columnconfigure(1, weight=11)
        buttonFrame.grid_rowconfigure(0, weight=1)

        cancel = Button(buttonFrame, text='Cancel', bg='#404040', fg='white', borderwidth=0,
                        command=lambda: swapScreens(h))
        cancel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

        join = Button(buttonFrame, text='Join', bg='#0f61d4', fg='white', borderwidth=0,
                      command=lambda: self.joinRoom(idEntry.get(), ipEntry.get()))
        join.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')

    def joinRoom(self, id, ip):
        global chats, contacts, user, net, h
        chats.insert(0, Chat(id, 'Unknown'))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        try:
            s.connect((ip, 8082))
            net.clients[chats[0].id] = Client(net, user, s, chats[0], contacts, h)
            threading.Thread(target=net.clients[chats[0].id].mainloop, daemon=True).start()
            swapScreens(h)
            h.changeChatFocus(chats[0])
        except socket.timeout:
            chats.pop(0)

class CreateRoom:
    def __init__(self, root):
        self.root = root
        self.id = genId()

    def render(self):
        global currentScreen
        currentScreen.append(self)

        self.main = Frame(self.root, bg='#303030')
        self.main.pack(fill=BOTH, expand=True)

        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)
        self.main.grid_columnconfigure(2, weight=1)

        container = Frame(self.main, width=350, height=200, bg='#101010')
        container.grid(row=1, column=1)

        container.grid_propagate(0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1,weight=2)
        container.grid_rowconfigure(2,weight=1)
        container.grid_columnconfigure(0, weight=1)

        title = Label(container, text='Create Room', bg='#101010', fg='white', font='Roboto 16')
        title.grid(row=0, column=0)

        textBoxFrame = Frame(container, bg='#101010')
        textBoxFrame.grid(row=1, column=0, sticky='NEW')

        textBoxFrame.grid_columnconfigure(0, weight=1)
        textBoxFrame.grid_columnconfigure(1, weight=1)
        textBoxFrame.grid_rowconfigure(0, weight=1)
        textBoxFrame.grid_rowconfigure(1, weight=1)

        idLabel = Label(textBoxFrame, text='ID:', bg='#101010', fg='white', font='Roboto 16')
        idLabel.grid(row=0, column=0, ipady=10)

        s = StringVar()
        s.set(self.id)
        idValue = Entry(textBoxFrame, state='readonly', textvariable=s, readonlybackground='#404040', fg='white',
                        font='Roboto 16')
        idValue.grid(row=0, column=1)
        idValue.config(relief='flat')

        nameLabel = Label(textBoxFrame, text='Name:', bg='#101010', fg='white', font='Roboto 16')
        nameLabel.grid(row=1, column=0, ipady=10)

        nameEntry = Entry(textBoxFrame, borderwidth=0, bg='#404040', font='Roboto 16', fg='#FFFFFF',
                          insertbackground='#909090')
        nameEntry.grid(row=1, column=1)

        buttonFrame = Frame(container, bg='#101010')
        buttonFrame.grid(row=2, column=0, sticky='NSEW')

        buttonFrame.grid_columnconfigure(0, weight=10)
        buttonFrame.grid_columnconfigure(1, weight=11)
        buttonFrame.grid_rowconfigure(0, weight=1)

        cancel = Button(buttonFrame, text='Cancel', bg='#404040', fg='white', borderwidth=0,
                        command=lambda: swapScreens(h))
        cancel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

        create = Button(buttonFrame, text='Create', bg='#0f61d4', fg='white', borderwidth=0,
                        command=lambda: self.createRoom(self.id, nameEntry.get()))
        create.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')

    def createRoom(self, id, name):
        global h, chats
        print(f'Created room with id: {id}')
        chats.insert(0, Chat(id, name))
        c.id = genId()
        net.hostList.append(chats[0])
        net.server.chatDict[chats[0].id] = chats[0]
        print(f'Added {id} to hostList.')
        swapScreens(h)
        h.changeChatFocus(chats[0])

class DeleteRoom:
    def __init__(self, root):
        self.root = root

    def render(self):
        global currentScreen
        currentScreen.append(self)

        self.main = Frame(self.root, bg='#303030')
        self.main.pack(fill=BOTH, expand=True)

        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)
        self.main.grid_columnconfigure(2, weight=1)

        container = Frame(self.main, width=350, height=150, bg='#101010')
        container.grid(row=1, column=1)

        container.grid_propagate(0)
        container.grid_rowconfigure(0,weight=2)
        container.grid_rowconfigure(1,weight=1)
        container.grid_columnconfigure(0, weight=1)

        textBoxFrame = Frame(container, bg='#101010')
        textBoxFrame.grid(row=0, column=0, sticky='NEW')

        textBoxFrame.grid_columnconfigure(0, weight=1)
        textBoxFrame.grid_columnconfigure(1, weight=1)
        textBoxFrame.grid_rowconfigure(0, weight=1)
        textBoxFrame.grid_rowconfigure(1, weight=1)

        msg = Label(textBoxFrame, text='Are you sure?', bg='#101010', fg='white', font='Roboto 16')
        msg.grid(row=0, column=0, ipady=10)

        buttonFrame = Frame(container, bg='#101010')
        buttonFrame.grid(row=1, column=0, sticky='NSEW')

        buttonFrame.grid_columnconfigure(0, weight=10)
        buttonFrame.grid_columnconfigure(1, weight=11)
        buttonFrame.grid_rowconfigure(0, weight=1)

        cancel = Button(buttonFrame, text='Cancel', bg='#404040', fg='white', borderwidth=0,
                        command=lambda: swapScreens(h))
        cancel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

        delete = Button(buttonFrame, text='Delete', bg='#0f61d4', fg='white', borderwidth=0,
                      command=lambda: self.deleteRoom())
        delete.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')

    def deleteRoom(self):
        global chats, h
        chat = h.viewedChat
        index = len(chats)-1-chats.index(chat)
        h.chatgfx[index].destroy()
        h.chatgfx.pop(index)
        chats.remove(chat)
        if len(chats) == 0:
            self.main.destroy()
            setup()
        else:
            swapScreens(h)
            h.changeChatFocus(chats[0])

class ChangeName:
    def __init__(self, root):
        self.root = root

    def render(self):
        global currentScreen, user
        currentScreen.append(self)

        self.main = Frame(self.root, bg='#303030')
        self.main.pack(fill=BOTH, expand=True)

        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)
        self.main.grid_columnconfigure(2, weight=1)

        container = Frame(self.main, width=350, height=100, bg='#101010')
        container.grid(row=1, column=1)

        container.grid_propagate(0)
        container.grid_rowconfigure(0,weight=2)
        container.grid_rowconfigure(1,weight=1)
        container.grid_columnconfigure(0, weight=1)

        textBoxFrame = Frame(container, bg='#101010')
        textBoxFrame.grid(row=0, column=0, sticky='NEW')

        textBoxFrame.grid_columnconfigure(0, weight=1)
        textBoxFrame.grid_columnconfigure(1, weight=1)
        textBoxFrame.grid_rowconfigure(0, weight=1)
        textBoxFrame.grid_rowconfigure(1, weight=1)

        nameLabel = Label(textBoxFrame, text='Username:', bg='#101010', fg='white', font='Roboto 16')
        nameLabel.grid(row=0, column=0, ipady=10, padx=5)

        s = StringVar()
        s.set(user.name)

        nameEntry = Entry(textBoxFrame, borderwidth=0, bg='#404040', font='Roboto 16', fg='#FFFFFF',
                          insertbackground='#909090', textvariable=s)
        nameEntry.grid(row=0, column=1, padx=5)

        buttonFrame = Frame(container, bg='#101010')
        buttonFrame.grid(row=1, column=0, sticky='NSEW')

        buttonFrame.grid_columnconfigure(0, weight=2)
        buttonFrame.grid_columnconfigure(1, weight=1)
        buttonFrame.grid_rowconfigure(0, weight=1)

        submit = Button(buttonFrame, text='Submit', bg='#0f61d4', fg='white', borderwidth=0,
                        command=lambda: self.setName(nameEntry.get()))
        submit.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')

    def setName(self, name):
        if name != '':
            global user
            user.name = name
            print(f'Updated name to {user.name}.')
            self.main.destroy()
            setup()

def swapScreens(new):
    global root, currentScreen, menubar
    for screen in currentScreen:
        screen.main.destroy()
        try:
            if type(screen) != ChangeName:
                m.menubar.destroy()
        except:
            continue
    currentScreen = []
    new.render()
    if type(new) != ChangeName:
        m.render()

def genId():
    return hex(random.randint(2**63+1,2**64))[2:].upper()

def setup():
    global chats, h, m, j, c
    # Start home screen
    if len(chats) > 0:
        h.render()
        h.changeChatFocus(chats[0])
        # Start menubar
        m.render()
    else:
        j.render()
        c.render()

def on_closing():
    with open('user.pkl', 'wb') as file:
        pickle.dump(user, file, pickle.HIGHEST_PROTOCOL)
    with open('contacts.pkl', 'wb') as file:
        pickle.dump(contacts, file)
    for chat in chats:
        chat.text = None
    with open('chats.pkl', 'wb') as file:
        pickle.dump(chats, file)
    root.destroy()
    net.server.run = False

if __name__ == '__main__':
    # Initialize tkinter window
    root = Tk()
    root.title('DeMsg')
    root.geometry('1280x720')
    root.resizable(True, True)
    root.minsize(1000,500)

    # Load stuff
    try:
        with open('user.pkl', 'rb') as file:
            user = pickle.load(file)
    except FileNotFoundError:
        print('User file does not exist, creating.')
        user = User()

    print(f"User ID is {user.id}")

    try:
        with open('contacts.pkl', 'rb') as file:
            contacts = pickle.load(file)
    except FileNotFoundError:
        print('Contacts file does not exist, creating.')
        contacts = {user.id: user}

    try:
        with open('chats.pkl', 'rb') as file:
            chats = pickle.load(file)
            for chat in chats:
                chat.text = StringVar()
                chat.text.set("\n".join([
                                        f"{contacts[chat.history[key][0]].name}: {chat.history[key][1]}"
                                        for key in sorted(chat.history.keys())
                                        ]))
    except FileNotFoundError:
        print('Chats file does not exist, creating.')
        chats = []

    # Set up screens
    m = MenuBar(root)
    h = Home(root)
    j = JoinRoom(root)
    c = CreateRoom(root)
    d = DeleteRoom(root)
    n = ChangeName(root)

    currentScreen = []

    if user.name == '':
        n.render()
    else:
        setup()
    net = Network(h)

    threading.Thread(target=net.start).start()

    root.protocol('WM_DELETE_WINDOW', on_closing)
    root.mainloop()
