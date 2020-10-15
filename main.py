import threading
from server import Server
import tkinter as tk
import tkinter.ttk as ttk
import pickle
import random

class User:
    def __init__(self, id='', addr='', name=''):
        if id == '':
            self.id = genId()
        self.addr = addr
        self.name = name

class Chat:
    def __init__(self, id):
        self.id = id
        self.members = []
        self.history = {}

class Home:
    def __init__(self, root):
        self.root = root
    def render(self):
        global currentScreen
        currentScreen = self

        self.main = tk.Frame(self.root)
        self.main.pack(fill=tk.BOTH, expand=True)

        leftSideBar = tk.Frame(self.main, width=300, bg='#101010')
        leftSideBar.grid(row=0,column=0,sticky='NESW')

        rightSideBar = tk.Frame(self.main, width=250, bg='#101010')
        rightSideBar.grid(row=0,column=2,sticky='NESW')

        self.main.rowconfigure(0,weight=1)
        self.main.grid_columnconfigure(1,weight=1)

        # scrollbar = tk.Scrollbar(leftSideBar)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        messageArea = tk.Frame(self.main, bg='#303030')
        messageArea.grid(row=0,column=1,sticky='NESW')

        msgBoxRect = tk.Frame(messageArea,height=40, bg='#404040')
        msgBoxRect.pack(side=tk.BOTTOM, fill=tk.X, padx=20,pady=20)

        msgBox = tk.Entry(msgBoxRect, bg='#404040', borderwidth=0, font='Roboto 16', fg='#FFFFFF', insertbackground='#909090')
        msgBoxRect.grid_columnconfigure(0,weight=9)
        msgBoxRect.grid_columnconfigure(1,weight=1)
        msgBox.grid(row=0, column=0, sticky='EW', pady=7, padx=5)

        send = tk.Button(msgBoxRect, text='Send', bg='#0f61d4',fg='white',borderwidth=0)
        send.grid(row=0, column=1, sticky='NSEW')

class JoinRoom:
    def __init__(self, root):
        self.root = root

    def render(self):
        global currentScreen
        currentScreen = self

        self.main = tk.Frame(self.root, bg='#303030')
        self.main.pack(fill=tk.BOTH, expand=True)

        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)
        self.main.grid_columnconfigure(2, weight=1)

        container = tk.Frame(self.main, width=350, height=150, bg='#101010')
        container.grid(row=1, column=1)

        container.grid_propagate(0)
        container.grid_rowconfigure(0,weight=2)
        container.grid_rowconfigure(1,weight=1)
        container.grid_columnconfigure(0, weight=1)

        textBoxFrame = tk.Frame(container, bg='#101010')
        textBoxFrame.grid(row=0, column=0, sticky='NEW')

        textBoxFrame.grid_columnconfigure(0, weight=1)
        textBoxFrame.grid_columnconfigure(1, weight=1)
        textBoxFrame.grid_rowconfigure(0, weight=1)
        textBoxFrame.grid_rowconfigure(1, weight=1)

        idLabel = tk.Label(textBoxFrame, text='ID:', bg='#101010', fg='white', font='Roboto 16')
        idLabel.grid(row=0, column=0, ipady=10)

        idEntry = tk.Entry(textBoxFrame, borderwidth=0, bg='#404040', font='Roboto 16', fg='#FFFFFF', insertbackground='#909090')
        idEntry.grid(row=0, column=1)

        ipLabel = tk.Label(textBoxFrame, text='IP:', bg='#101010', fg='white', font='Roboto 16')
        ipLabel.grid(row=1, column=0, ipady=10)

        ipEntry = tk.Entry(textBoxFrame, borderwidth=0, bg='#404040', font='Roboto 16', fg='#FFFFFF', insertbackground='#909090')
        ipEntry.grid(row=1, column=1)

        buttonFrame = tk.Frame(container, bg='#101010')
        buttonFrame.grid(row=1, column=0, sticky='NSEW')

        buttonFrame.grid_columnconfigure(0, weight=10)
        buttonFrame.grid_columnconfigure(1, weight=11)
        buttonFrame.grid_rowconfigure(0, weight=1)

        cancel = tk.Button(buttonFrame, text='Cancel', bg='#404040', fg='white', borderwidth=0, command=lambda: swapScreens(h))
        cancel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

        join = tk.Button(buttonFrame, text='Join', bg='#0f61d4', fg='white', borderwidth=0)
        join.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')

class CreateRoom:
    def __init__(self, root):
        self.root = root
        self.id = genId()

    def render(self):
        global currentScreen
        currentScreen = self

        self.main = tk.Frame(self.root, bg='#303030')
        self.main.pack(fill=tk.BOTH, expand=True)

        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)
        self.main.grid_columnconfigure(2, weight=1)

        container = tk.Frame(self.main, width=350, height=100, bg='#101010')
        container.grid(row=1, column=1)

        container.grid_propagate(0)
        container.grid_rowconfigure(0,weight=2)
        container.grid_rowconfigure(1,weight=1)
        container.grid_columnconfigure(0, weight=1)

        textBoxFrame = tk.Frame(container, bg='#101010')
        textBoxFrame.grid(row=0, column=0, sticky='NEW')

        textBoxFrame.grid_columnconfigure(0, weight=1)
        textBoxFrame.grid_columnconfigure(1, weight=1)
        textBoxFrame.grid_rowconfigure(0, weight=1)
        textBoxFrame.grid_rowconfigure(1, weight=1)

        idLabel = tk.Label(textBoxFrame, text='ID:', bg='#101010', fg='white', font='Roboto 16')
        idLabel.grid(row=0, column=0, ipady=10)

        s = tk.StringVar()
        s.set(self.id)
        idValue = tk.Entry(textBoxFrame, state='readonly', textvariable=s, readonlybackground='#404040', fg='white', font='Roboto 16')
        idValue.grid(row=0, column=1)
        idValue.config(relief='flat')

        buttonFrame = tk.Frame(container, bg='#101010')
        buttonFrame.grid(row=1, column=0, sticky='NSEW')

        buttonFrame.grid_columnconfigure(0, weight=10)
        buttonFrame.grid_columnconfigure(1, weight=11)
        buttonFrame.grid_rowconfigure(0, weight=1)

        cancel = tk.Button(buttonFrame, text='Cancel', bg='#404040', fg='white', borderwidth=0, command=lambda: swapScreens(h))
        cancel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

        create = tk.Button(buttonFrame, text='Create', bg='#0f61d4', fg='white', borderwidth=0, command=lambda: hostRoom(self.id))
        create.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')

class ChangeName:
    def __init__(self, root):
        self.root = root

    def render(self):
        global currentScreen, user
        currentScreen = self

        self.main = tk.Frame(self.root, bg='#303030')
        self.main.pack(fill=tk.BOTH, expand=True)

        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)
        self.main.grid_columnconfigure(2, weight=1)

        container = tk.Frame(self.main, width=350, height=100, bg='#101010')
        container.grid(row=1, column=1)

        container.grid_propagate(0)
        container.grid_rowconfigure(0,weight=2)
        container.grid_rowconfigure(1,weight=1)
        container.grid_columnconfigure(0, weight=1)

        textBoxFrame = tk.Frame(container, bg='#101010')
        textBoxFrame.grid(row=0, column=0, sticky='NEW')

        textBoxFrame.grid_columnconfigure(0, weight=1)
        textBoxFrame.grid_columnconfigure(1, weight=1)
        textBoxFrame.grid_rowconfigure(0, weight=1)
        textBoxFrame.grid_rowconfigure(1, weight=1)

        nameLabel = tk.Label(textBoxFrame, text='Username:', bg='#101010', fg='white', font='Roboto 16')
        nameLabel.grid(row=0, column=0, ipady=10, padx=5)

        s = tk.StringVar()
        s.set(user.name)

        nameEntry = tk.Entry(textBoxFrame, borderwidth=0, bg='#404040', font='Roboto 16', fg='#FFFFFF', insertbackground='#909090', textvariable=s)
        nameEntry.grid(row=0, column=1, padx=5)

        buttonFrame = tk.Frame(container, bg='#101010')
        buttonFrame.grid(row=1, column=0, sticky='NSEW')

        buttonFrame.grid_columnconfigure(0, weight=2)
        buttonFrame.grid_columnconfigure(1, weight=1)
        buttonFrame.grid_rowconfigure(0, weight=1)

        submit = tk.Button(buttonFrame, text='Submit', bg='#0f61d4', fg='white', borderwidth=0, command=lambda: self.setName(nameEntry.get()))
        submit.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')

    def setName(self, name):
        if name != '':
            global user
            user.name = name
            with open('user.pkl', 'wb') as file:
                pickle.dump(user, file, pickle.HIGHEST_PROTOCOL)
            print(f'Updated name to {user.name}.')
            swapScreens(h)


def swapScreens(new):
    global root, currentScreen
    currentScreen.main.destroy()
    new.render()

def genId():
    return hex(random.randint(2**63+1,2**64))[2:].upper()

def hostRoom(id):
    print(f'Hosting room with id: {id}')
    threading.Thread(target=lambda: Server(80)).start()
    chats.append(Chat(id))
    c.id = genId()
    swapScreens(h)

if __name__ == '__main__':
    # Initialize tkinter window
    root = tk.Tk()
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
        with open('user.pkl', 'wb') as file:
            pickle.dump(user, file, pickle.HIGHEST_PROTOCOL)

    try:
        with open('chats.pkl', 'rb') as file:
            chats = pickle.load(file)
    except FileNotFoundError:
        print('Chats file does not exist, creating.')
        chats = []
        with open('chats.pkl', 'wb') as file:
            pickle.dump(chats, file, pickle.HIGHEST_PROTOCOL)

    # Set up screens
    h = Home(root)
    j = JoinRoom(root)
    c = CreateRoom(root)
    n = ChangeName(root)

    if user.name == '':
        n.render()
    else:
        # Start home screen
        h.render()

    # Set up menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    profile = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Profile', menu=profile)
    profile.add_command(label='Change Name', command=lambda: swapScreens(n))
    rooms = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rooms', menu=rooms)
    rooms.add_command(label='Create Room', command=lambda: swapScreens(c))
    rooms.add_command(label='Join Room', command=lambda: swapScreens(j))

    root.mainloop()
