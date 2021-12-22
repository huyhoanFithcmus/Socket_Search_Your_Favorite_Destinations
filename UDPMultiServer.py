import socket
import threading
from datetime import datetime
import json
from tkinter.constants import FIRST, N
import tkinter as tk
from tkinter import *

class UDPServer:
    ''' A simple UDP Server '''
    def __init__(self, host, port):

        self.host = host    # Host address
        self.port = port    # Host port
        self.sock = None    # Socket

    def printwt(self, msg):

        ''' Print message with current date and time '''
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{current_date_time}] {msg}')
    def configure_server(self):


        ''' Configure the server '''
        # create UDP socket with IPv4 addressing

        self.printwt('Creating socket...')
        self.printwt('Socket created')
        # bind server to the address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host,self.port))
        self.printwt(f'Binding server to {self.host}:{self.port}...')
        self.printwt(f'Server binded to {self.host}:{self.port}')

    def handle_request(self, data, client_address):

        ''' Handle the client '''
        # handle request

        name = data.decode('utf-8')
        self.printwt(f'[ REQUEST from {client_address} ]')
        print(name)
        # send response to the client
        resp = ""
        
        #time.sleep(3)
        self.printwt(f'[ RESPONSE to {client_address} ]')
        self.sock.sendto(resp.encode('utf-8'), client_address)
        print(resp)
    def wait_for_client(self):

        ''' Wait for a client '''
        try:
            # receive message from a client

            data, client_address = self.sock.recvfrom(1024)
            # handle client's request

            self.handle_request(data, client_address)
        except OSError as err:
            self.printwt(err)
    def shutdown_server(self):
        ''' Shutdown the UDP server '''
        self.printwt('Shutting down server...')
        self.sock.close()

class UDPServerMultiClient(UDPServer):
    ''' A simple UDP Server for handling multiple clients '''

    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket_lock = threading.Lock()
    def sendFile(self,fileName, addr):
        file = open(fileName, 'rb')
        data = file.read(4096)

        while data:
            with self.socket_lock:
                self.sock.sendto(data, addr)
            data = file.read(4096)

        self.sock.sendto(data, addr) 
        file.close()
    def queryLocation (self,addr, str):
        '''exchange information with the client about json'''
        data = ""

        with open('data.json', encoding = 'utf8') as file_name:
            data = json.load(file_name)

        for item in data['place']:
            if (str == item['id'] or str == ""):
                msg = "--------------------------------------------"
                with self.socket_lock:    
                    self.sock.sendto(msg.encode('utf-8'), addr)
                msg = "ID: "+ item['id']
                with self.socket_lock:
                    self.sock.sendto(msg.encode('utf-8'), addr)
                msg = "Name: "+ item['name']
                with self.socket_lock:
                    self.sock.sendto(msg.encode('utf-8'), addr)
                msg = "Abbreviation: " + item['abbreviation']
                with self.socket_lock:
                    self.sock.sendto(msg.encode('utf-8'), addr)
                msg ="Coordinates is "+ item['coordinate']['longitude']+ " and "+ item['coordinate']['latitude']
                with self.socket_lock:
                    self.sock.sendto(msg.encode('utf-8'), addr)
                msg = "Description: "+ item['description']
                with self.socket_lock:
                    self.sock.sendto(msg.encode('utf-8'), addr)
                for i in range(0, len(item['image'])):
                    msg = "Picture: "+ item['image'][i]
                    with self.socket_lock:
                        self.sock.sendto(msg.encode('utf-8'), addr)
                msg = "_____________________________________________"
                with self.socket_lock:
                    self.sock.sendto(msg.encode('utf-8'), addr)
        msg = "done"
        with self.socket_lock:
            self.sock.sendto(msg.encode('utf-8'), addr)
        
    def handle_request(self, data, client_address):
        ''' Handle the client '''
        # handle request
        name = data.decode('utf-8')
        if name == 'quit':
            resp = "Disconnected to " + str(client_address)  
        elif (name == "Danh Sach"):
            self.queryLocation(client_address, "")
            resp ="DONE"
        elif "tim kiem ID: " in name:
            name = name.replace('tim kiem ID: ','')
            self.queryLocation(client_address, name)
            resp = "Find " + name + " DONE"
        elif (name == "Tim kiem"):
            resp = "Finding...."
        elif ".jpg" in name or ".docx" in name:
            self.sendFile(name, client_address)
            resp = "Send Image Done"
        else:
            resp = "None"
            self.sock.sendto(resp.encode('utf-8'), client_address)
        self.printwt(f'[ REQUEST from {client_address} ]')
        print(name)

        self.printwt(f'[ RESPONSE to {client_address} ]')
        print(resp)
    
    def wait_for_client(self):
        ''' Wait for clients and handle their requests '''
        try:
            while True: # keep alive
                try: # receive request from client
                    data, client_address = self.sock.recvfrom(1024)
                    c_thread = threading.Thread(target = self.handle_request,args = (data, client_address))
                    c_thread.daemon = True
                    c_thread.start()
                    
                except OSError as err:
                    self.printwt(err)
        
        except KeyboardInterrupt:
            self.shutdown_server()

def main():
    ''' Create a UDP Server and handle multiple clients simultaneously '''
    
    udp_server_multi_client = UDPServerMultiClient('127.0.0.1', 6789)
    udp_server_multi_client.configure_server()
    udp_server_multi_client.wait_for_client()

if __name__ == '__main__':
    main()