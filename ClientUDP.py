from contextlib import nullcontext
import socket
import tkinter as tk
from tkinter import *
import tkinter.ttk
from tkinter.constants import S
from typing import Sized
from PIL import Image, ImageTk
from image import runImage
from tkinter import ttk


class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.master.title('Địa Điểm Yêu Thích')
        #self.master.geometry('800x450+100+10')  # size of the main window
        self.master.geometry('980x670+10+10')  # size of the main window
        self.master.rowconfigure(0, weight=10)  # make the CanvasImage widget expandable
        self.master.columnconfigure(0, weight=10)
        self.vsb = nullcontext
        self.canvas = nullcontext
        self.frame = nullcontext

    def populate(self, type):
        self.destroy()
        self.canvas = tk.Canvas(self, borderwidth=0, background="#17202A", bg= '#17202A')
        self.frame = tk.Frame(self.canvas, background="#17202A", bg='#17202A')
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
 
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, bg= 'blue')
        self.canvas.configure(yscrollcommand=self.vsb.set)
        listImage = []
        self.vsb.pack(side="right", fill="y")
        '''Put in some fake data'''
        data = client.recvfrom(4096)
        str_data = data[0].decode(FORMAT)
        i = 0
        def clicked(listImg):
            for i in range(0, len(listImg)):
                listImg[i] = listImg[i].replace('Picture: ','')
                client.sendto(listImg[i].encode(FORMAT),server_address)
                listImg[i] = listImg[i].replace('images/','')
                print(listImg[i]) 
                self.receiveFile(listImg[i])
            runImage(listImg)
            
        if (str_data == "done"):
            tk.Label (self.frame, text="Access data not found!!", font=("Arial Bold", 20), bg= '#17202A',fg = "#EAECEE").grid(row=i, column=1)
        while (str_data != "done"):
            print(str_data)
            tk.Label (self.frame, text=str_data, font=("Arial Bold", 10), bg= '#17202A',fg = "#EAECEE").grid(row=i, column=1)
            if (str_data == "_____________________________________________"):
                tk.Button(self.frame, text=" DOWNLOAD ",bg="#EAECEE", fg="black", command= lambda val = listImage:clicked(val)).grid(row=i,column=15)
            if "Picture: " in str_data:
                listImage.append(str_data)
            data = client.recvfrom(4096)
            str_data = data[0].decode(FORMAT)
            i = i+ 1
        def clickBack ():
            if type == "T":
                self.search()
            elif type == "S":
                self.populateList()
        Backbutton = tk.Button(self.frame, text="Back", font=("Arial Bold", 12), command=lambda: clickBack())
        Backbutton.grid(row=i, column=0, pady=5)

        self.grid(column=0, row=0)#, sticky='NS')#side="left", fill="both", expand=True)
        self.grid(sticky='nswe')  # make frame container sticky
        self.rowconfigure(0, weight=1)  # make canvas expandable
        self.columnconfigure(0, weight=1)

    def populateList(self):
        self.destroy()
        client.sendto("Danh Sach".encode(FORMAT),server_address)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#17202A", bg= '#17202A')
        self.frame = tk.Frame(self.canvas, background="#17202A", bg='#17202A')
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
 
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, bg= 'blue')
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        '''Put in some fake data'''
        data = client.recvfrom(4096)
        str_data = data[0].decode(FORMAT)
        i = 0
        count = 1
        def clicked(str):
            msg = "tim kiem " + str
            client.sendto(msg.encode(FORMAT),server_address)
            print(msg)
            self.result("S")
        def clickedDown(str):
            client.sendto(str.encode(FORMAT),server_address)
            #print(msg) 
            self.receiveFile('List.docx')
        if (str_data == "done"):
            tk.Label (self.frame, text="Access data not found!!", font=("Arial Bold", 20), bg= '#17202A',fg = "#EAECEE").grid(row=i, column=1)
        tk.Button(self.frame, text=" DOWNLOAD ALL ",bg="#EAECEE", fg="black", command= lambda val = "data.docx":clickedDown(val)).grid(row=i,column=0,pady=5)
        while (str_data != "done"):
            print(str_data)
            tk.Label (self.frame, text=str_data, font=("Arial Bold", 10), bg= '#17202A' ,fg = "#EAECEE").grid(row=i, column=1)
            if (str_data == "--------------------------------------------"):
                tk.Label (self.frame, text=" %s " %count, font=("Arial Bold", 20), bg= '#17202A',fg = "#EAECEE").grid(row=i, column=1)
            if (str_data == "_____________________________________________"):
                tk.Label(self.frame, text="", bg='#17202A',fg = "#EAECEE").grid(row=i, column=1)
                bt =tk.Button(self.frame, text=" GO ",bg="#EAECEE", fg="black", command= lambda val = str:clicked(val)).grid(row=i,column=0, pady=5)
                count = count + 1
            i = i + 1

            if "ID: " in str_data:
                str = str_data
            data = client.recvfrom(4096)
            str_data = data[0].decode(FORMAT)
        Backbutton = tk.Button(self.frame, text="Back", font=("Arial Bold", 12), command=lambda: self.mainMenu())
        Backbutton.grid(row=i, column=0, pady=5)
        self.grid(column=0, row=0)
        self.grid(sticky='nswe')  # make frame container sticky
        self.rowconfigure(0, weight=1)  # make canvas expandable
        self.columnconfigure(0, weight=1)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=800,height=600)

    def search(self):
        client.sendto("Tim kiem".encode(FORMAT),server_address)
        self.destroy()
        self.canvas = tk.Canvas(self, borderwidth=0, background="#17202A", bg= '#17202A')
        self.frame = tk.Frame(self.canvas, background="#17202A", bg='#17202A')
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
 
        self.frame.bind("<Configure>", self.onFrameConfigure)

        label = tk.Label(self.frame, text="\n            Enter ID           \n", font=("Arial Bold", 24))
        label.grid(row=0, column=0, pady=5)

        txt = tk.Entry(self.frame, width = 35, bg = '#dff0ee')
        txt.grid(row=3, column=0, pady=5)
        
        def clicked():
            msg = "tim kiem ID: " + txt.get()
            client.sendto(str.encode(msg),server_address)
            self.result("T")

        btn = tk.Button(self.frame, text="     search     ", font=("Arial Bold", 12), command=lambda: clicked())
        btn.grid(row=5, column=0, pady=5)

        Backbutton = tk.Button(self.frame, text="Back", font=("Arial Bold", 12), command=lambda: self.mainMenu())
        Backbutton.grid(row=8, column=0, padx=10)
        
        self.grid(column=0, row=0)
        self.grid(sticky='nswe')  # make frame container sticky
        self.rowconfigure(0, weight=1)  # make canvas expandable
        self.columnconfigure(0, weight=1)
    
    def destroy (self):
        if self.vsb != nullcontext:
            self.vsb.destroy()
        if self.canvas != nullcontext:
            self.canvas.destroy()
        if self.frame != nullcontext:
            self.frame.destroy()
    
    def result(self, type):
        self.destroy()
        self.populate(type)
        
    def receiveFile(self,fileName):
        file = open(fileName, "wb")
        chuck = client.recvfrom(4096)
        while chuck[0]:
            file.write(chuck[0])
            chuck = client.recvfrom(4096)

        print("Receive File Success")
        file.close()
    
    def mainMenu (self):
        self.destroy()
        self.canvas = tk.Canvas(self, borderwidth=0, background="#17202A", bg= '#17202A')
        self.frame = tk.Frame(self.canvas, background="#17202A", bg='#17202A')
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
 
        self.frame.bind("<Configure>", self.onFrameConfigure)

        label = tk.Label(self.frame, text="Trang chủ địa điểm yêu thích", font=("Arial Bold", 24))
        label.grid(row=0, column=0, pady=5)
        
        Listbutton = tk.Button(self.frame, text="Danh sách địa điểm", font=("Arial Bold", 12), command=lambda: self.populateList())
        Listbutton.grid(row=1, column=0, pady=5)

        Searchbutto = tk.Button(self.frame, text="Tìm kiếm địa điểm", font=("Arial Bold", 12), command=lambda: self.search())
        Searchbutto.grid(row=2, column=0, pady=5)

        Infobutton = tk.Button(self.frame, text="Thong tin nhom", font=("Arial Bold", 12), command=lambda: self.creator())
        Infobutton.grid(row=3, column=0, pady=5)

        self.grid(column=0, row=0)
        self.grid(sticky='nswe')  # make frame container sticky
        self.rowconfigure(0, weight=1)  # make canvas expandable
        self.columnconfigure(0, weight=1)
    
    def creator (self):
        self.destroy()
        self.canvas = tk.Canvas(self, borderwidth=0, background="#17202A", bg= '#17202A')
        self.frame = tk.Frame(self.canvas, background="#17202A", bg='#17202A')
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
 
        self.frame.bind("<Configure>", self.onFrameConfigure)

        label = tk.Label(self.frame, text="Danh Sach các thành viên", font=("Arial Bold", 24))
        label.grid(row=0, column=0, pady=5)

        label = tk.Label(self.frame, text="Nguyễn Đình Văn - 20127662", font=("Arial Bold", 18))
        label.grid(row=1, column=0, pady=5)
        
        label = tk.Label(self.frame, text="Nguyễn Huy Hoàn - 20127166", font=("Arial Bold", 18))
        label.grid(row=2, column=0, pady=5)

        label = tk.Label(self.frame, text="Lưu Minh Phát - 20127061", font=("Arial Bold", 18))
        label.grid(row=3, column=0, pady=5)

        Backbutton = tk.Button(self.frame, text="Back", font=("Arial Bold", 12), command=lambda: self.mainMenu())
        Backbutton.grid(row=5, column=4, pady=5)

        self.grid(column=0, row=0)
        self.grid(sticky='nswe')  # make frame container sticky
        self.rowconfigure(0, weight=1)  # make canvas expandable
        self.columnconfigure(0, weight=1)

HOST = '127.0.0.1'  
PORT = 6789        
FORMAT = "utf8"
FONT = ("Calibri", 15, "bold")
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (HOST, PORT)
   

def main ():
    print('connecting to %s port ' + str(server_address))
    root=tk.Tk()
    example = Example(root)    
    try:
        example.mainMenu()
        example.mainloop()
        # while True:
        #     msg = input('Client: ')
        #     client.sendto(str.encode(msg),server_address)
            
        #     if msg == "quit":
        #         break
        #     elif msg == "Danh Sach":
        #         example.process(msg)
        #     elif msg == "Tim kiem":
        #         example.process(msg)
        #     elif ".jpg" in msg:
        #         example.receiveFile('server_image.jpg')
        #     elif ".docx" in msg:
        #         example.receiveFile('server_list.docx')
        #     else:
        #         data = client.recvfrom(1024)
        #         print('Server: ', data[0].decode(FORMAT))
        #         if (data[0].decode(FORMAT) == "error"):
        #             break
    except:
        print ("Error!")
    finally:
        client.close()

if __name__ == '__main__':
    main()