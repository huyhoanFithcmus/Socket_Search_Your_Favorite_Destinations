import socket
import sys
import threading
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import ttk


class GUI_client(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        # ten cua client window
        self.title("name")
        # chieu dai va chieu rong cua window
        self.geometry("500x500")
        # resize window
        self.resizable(False, False)
        #logo window
        self.iconbitmap('logo.ico')

# main function
if __name__ == "__main__":
    #input IP
    ip = input("Nhap IP cua server: ")
    #input port
    port = input("Nhap port cua server: ")
    app = GUI_client()
    app.mainloop()


