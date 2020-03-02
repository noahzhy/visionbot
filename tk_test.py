import tkinter as tk
from tkinter import Message, Tk


sec_timer = 2

top = Tk()
top.title('Device Status')
Message(top, text='No camera!', padx=20, pady=20).pack()
top.after(sec_timer*1000, top.destroy)

top.mainloop()
top.withdraw()