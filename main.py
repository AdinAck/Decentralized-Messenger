import tkinter as tk
import tkinter.ttk as ttk

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

        # Set up menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        menubar2 = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Menu', menu=menubar2)
        menubar2.add_command(label='Create Room', command=lambda: swapScreens(c))
        menubar2.add_command(label='Join Room', command=lambda: swapScreens(j))

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

        ipLabel = tk.Label(textBoxFrame, text='IP:', bg='#101010', fg='white', font='Roboto 16')
        ipLabel.grid(row=1, column=0, ipady=10)

        buttonFrame = tk.Frame(container, bg='#101010')
        buttonFrame.grid(row=1, column=0, sticky='NSEW')

        buttonFrame.grid_columnconfigure(0, weight=10)
        buttonFrame.grid_columnconfigure(1, weight=11)
        buttonFrame.grid_rowconfigure(0, weight=1)

        cancel = tk.Button(buttonFrame, text='Cancel', bg='#404040', fg='white', borderwidth=0, command=lambda: swapScreens(h))
        cancel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

        create = tk.Button(buttonFrame, text='Create', bg='#0f61d4', fg='white', borderwidth=0)
        create.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')


def swapScreens(new):
    global root, currentScreen
    currentScreen.main.destroy()
    new.render()

if __name__ == '__main__':
    # Initialize tkinter window
    root = tk.Tk()
    root.title('DeMsg')
    root.geometry('1280x720')
    root.resizable(True, True)
    root.minsize(1000,500)

    # Set up screens
    h = Home(root)
    j = JoinRoom(root)
    c = CreateRoom(root)

    # Start home screen
    h.render()

    root.mainloop()
