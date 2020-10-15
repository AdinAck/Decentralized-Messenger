import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()
root.title('DeMsg')
root.geometry('1280x720')
root.resizable(True, True)
root.minsize(750,500)

sideBar = tk.Frame(root, bg='#101010')
sideBar.grid(row=0,column=0,sticky='NESW')
root.rowconfigure(0,weight=1)
root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(1,weight=3)

main = tk.Frame(root, bg='#303030')
main.grid(row=0,column=1,sticky='NESW')

msgBoxRect = tk.Frame(main,height=40, bg='#404040')
msgBoxRect.pack(side=tk.BOTTOM, fill=tk.X, padx=20,pady=20)
msgBoxRect.grid_propagate(0)

msgBox = tk.Entry(msgBoxRect, bg='#404040', borderwidth=0, font='Roboto 16', fg='#FFFFFF', insertbackground='#909090')
msgBoxRect.grid_columnconfigure(0,weight=9)
msgBoxRect.grid_columnconfigure(1,weight=1)
msgBox.grid(row=0, column=0, sticky='EW', pady=7, padx=5)

send = ttk.Button(msgBoxRect, text='Send')
send.grid(row=0, column=1, sticky='NSEW')

root.mainloop()
