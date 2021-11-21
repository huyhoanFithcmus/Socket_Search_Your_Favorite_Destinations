import socket
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

EXIT = 'exit'

class GUI_client(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("TRA CỨU ĐỊA ĐIỂM YÊU THÍCH")
        self.geometry("500x250")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.stop)
        self.label = tkinter.Label(self, text="TRA CỨU ĐỊA ĐIỂM YÊU THÍCH", font=("Arial", 15))
        self.label.pack()

        window_box = tkinter.Frame(self)
        window_box.pack(side=TOP, fill=BOTH, expand=True)
        window_box.grid_rowconfigure(0, weight=1)
        window_box.grid_columnconfigure(0, weight=1)

        self.frame = {}
        for F in (Main_page, Login_page):
            self.frame[F] = F(window_box, self)
            self.frame[F].grid(row=0, column=0, sticky="nsew")
        self.show_slide(Login_page)
    
    def show_slide(self, window_box):
        frame = self.frame[window_box]
        if window_box == Main_page:
            self.geometry("777x777")
            frame.tkraise()
        else:
            self.geometry("666x666")
            frame.tkraise()  

    def quit_Closed(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            try:
                choice = EXIT
                self.client.send(choice.encode('utf-8'))
                self.client.close()
            except:
                window = tkinter.Tk()
                window.wm_withdraw()
                window.geometry("1x1+200+200")
                messagebox.showwarning('Not responding','Disconnected')
                self.client.close()
                self.sys.exit(0)
    
    def Login(self, nowFrame, socket):
        try:
            UserName = nowFrame.boxUser.get()
            Password = nowFrame.boxPassword.get()

            print ("Username: ", UserName)
            print ("Password: ", Password)

            if Password == "":
                nowFrame.Notice["text"] = "Mật khẩu không thể để trống!"
                return
            elif UserName == "":
                nowFrame.Notice["text"] = "Tài khoản không thể để trống!"
                return
            elif UserName == "" and Password == "":
                nowFrame.Notice["text"] = "Tài khoản và mật khẩu trống"
                return

            choice = 'login'
            socket.sendall(choice.encode('utf-8'))
            
            # Sock send user
            socket.sendall(UserName.encode('utf-8'))
            socket.recv(1024)
            print ("Has responded")

            # Sock send Password
            socket.sendall(Password.encode('utf-8'))
            socket.recv(1024)
            print ("Has responded")

            check = socket.recv(1024).decode('utf-8')
            if check == '1':
                self.nowSlide(Main_page)
            elif check == '2':
                nowFrame.Notice["text"] = "Mật khẩu và tài khoản có thể sai"
            elif check == '0':
                nowFrame.Notice["text"] = "Bạn đã đăng nhập sẵn rồi!"

        except: 
            nowFrame.Notice["text"] = "Server không thể phản hồi!"
            print("Lỗi server không phản hồi!")
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
            self.socket.close()
            self.sys.exit(0)

    def Register(self, nowFrame, socket):
        try:
            UserName = nowFrame.boxUser.get()
            Password = nowFrame.boxPassword.get()

            if Password == "":
                nowFrame.Notice["text"] = "Mật khẩu không thể để trống!"
                return
            elif UserName == "":
                nowFrame.Notice["text"] = "Tài khoản không thể để trống!"
                return
            elif UserName == "" and Password == "":
                nowFrame.Notice["text"] = "Tài khoản và mật khẩu trống"
                return

            choice = 'signup'
            socket.sendall(choice.encode('utf-8'))

            socket.sendall(UserName.encode('utf-8'))
            socket.recv(1024)
            print ("Has responded")

            socket.sendall(Password.encode('utf-8'))
            socket.recv(1024)
            print ("Has responded")
            
            check = socket.recv(1024).decode('utf-8')
            if check == "True":
                self.nowSlide(Main_page)
            elif check == "Already":
                nowFrame.Notice["text"] = "Tài khoản đã đăng ký và có người sử dụng"
            elif check == "False":
                nowFrame.Notice["text"] = "Tài khoản đã đăng ký"
            
        except:
            nowFrame.Notice["text"] = "Server không phản hồi, ngắt kết nối"
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')


    def start(self):
        self.mainloop()

    def stop(self):
        self.destroy()

class Main_page(tkinter.Frame): 
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tkinter.Label(self, text="Main Page", font=("Arial", 15))
        self.label.pack()
        self.button = tkinter.Button(self, text="Back", command=self.back)
        self.button.pack()

    def back(self):
        self.controller.show_slide(Login_page)

class Login_page(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tkinter.Label(self, text= "\nĐĂNG NHẬP THÔNG TIN\n", font = ("Arial", 15), fg = '#5a5865', bg = "#e1dcfd").grid(row = 3, column = 1)
        User = tkinter.Label(self, text = "\tTÀI KHOẢN", fg = '#5a5865', bg = "#e1dcfd", font='Calibri 12 bold').grid(row = 4, column = 0)
        Passw = tkinter.Label(self, text = "\tMẬT KHẨU ", fg = '#5a5865', bg = "#e1dcfd", font='Calibri 12 bold').grid(row = 5, column = 0)

        self.Notice = tkinter.Label(self, text = "", bg = "#e1dcfd", fg = 'red')
        self.boxUser = tkinter.Entry(self, width = 35, bg = '#dff0ee')
        self.boxUser.grid(row = 4, column = 1) 
        self.boxUser.configure(bg = "#e1dcfd") 
        self.boxPassword = tkinter.Entry(self, width = 35, bg = '#dff0ee')
        self.boxPassword.grid(row = 5, column = 1)
        self.boxPassword.configure(bg = "#e1dcfd")


        self.button2 = tkinter.Button(self, text="Register", bg = "#5a5865", fg = '#dff0ee' ,font=("Arial", 15), command=lambda: self.controller.Register(self, self.controller.client))
        self.button2.configure(width = 10)
        self.button2.grid(column = 1, row = 7)
        self.button1 = tkinter.Button(self, text="Login",  bg = "#5a5865", fg = '#dff0ee' ,font=("Arial", 15), command=lambda: self.controller.Login(self, self.controller.client))
        self.button1.configure(width = 10)
        self.button1.grid(column = 1, row = 9)
    
# main function
if __name__ == "__main__":
    #input IP
    ip = input("Nhap IP cua server: ")
    #input port
    port = input("Nhap port cua server: ")
    app = GUI_client()
    app.mainloop()


    


