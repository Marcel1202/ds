import socket 
from threading import Thread
import os
import math



class Socket_Server:
    def __init__(self):
        self.s1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2=self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def Thread2(self): #Thread the server so both Automated Bartender and Photo Encoder have the different Sockets
        self.threads=[]
        hostname=['localhost','localhost']
        port=[8001,8002]

        process=Thread(target=self.auto_bar,args=[hostname[0],port[0]])
        process.start()
        self.threads.append(process)

        process=Thread(target=self.photo_encoder,args=[hostname[1],port[1]])
        process.start()
        self.threads.append(process)

        print(self.threads)
    

    def auto_bar(self,hostname,port): #deals with requests from Automated Bartender
        self.s1.bind((hostname,port))
        self.s1.listen()
        
        while True:
            s,addr=self.s1.accept()
            received=s.recv(1024)

            if received.decode()=='GiveEncodings':
                print(f'Client on port {port} is asking to get Encodings')
                if os.path.exists('Files/Encodings'):
                    file_size=str(os.path.getsize('Files/Encodings')).encode()
                    s.send(file_size)
                    received1=s.recv(1024)
                    if received1.decode()=='Send':
                        with open('Files/Encodings','rb') as fp:
                            l=fp.read(1024)
                            while l:
                                s.send(l)
                                l=fp.read(1024)
                        s.close()
                else:
                    file_size='0'
                    s.send(file_size.encode())
                    s.close()

            elif received.decode()=='SendingEncodings':
                print(f'Client on port {port} is asking to send for Encodings')
                file_size=s.recv(1024)
                m=math.ceil(math.log(int(file_size.decode()),1024))
                s.send('Send'.encode())
                with open('Files/Encodings','wb') as fp:
                    l=s.recv(1024)
                    while l:
                        fp.write(l)
                        l=s.recv(1024)
                s.close()
            
            if received.decode()=='GiveUserDictionary':
                print(f'Client on port {port} is asking to receive for Drink List')
                if os.path.exists('Files/Client_Dict'):
                    file_size=str(os.path.getsize('Files/Client_Dict')).encode()
                    s.send(file_size)
                    received1=s.recv(1024)
                    if received1.decode()=='Send':
                        with open('Files/Client_Dict','rb') as fp:
                            l=fp.read(1024)
                            while l:
                                s.send(l)
                                l=fp.read(1024)
                        s.close()
                else:
                    file_size='0'
                    s.send(file_size.encode())
                    s.close()

            elif received.decode()=='SendingUserDictionary':
                print(f'Client on port {port} is asking to send for Drink List')
                file_size=s.recv(1024)
                s.send('Send'.encode())
                with open('Files/Client_Dict','wb') as fp:
                    l=s.recv(1024)
                    while l:
                        fp.write(l)
                        l=s.recv(1024)
                    s.close()
                        
                s.close()

    def photo_encoder(self,hostname,port): #deals with requests from Photo Encoder
        self.s2.bind((hostname,port))
        self.s2.listen()
        
        
        while True:
            s,addr=self.s2.accept()
            received=s.recv(1024)


            if received.decode()=='GiveEncodings':
                if os.path.exists('Files/Encodings'):
                    print(f'Client on port {port} is asking to receive Encodings')
                    file_size=str(os.path.getsize('Files/Encodings')).encode()
                    s.send(file_size)
                    received1=s.recv(1024)
                    if received1.decode()=='Send':
                        with open('Files/Encodings','rb') as fp:
                            l=fp.read(1024)
                            while l:
                                s.send(l)
                                l=fp.read(1024)
                        s.close()
                else:
                    file_size='0'
                    s.send(file_size.encode())
                    s.close()

            elif received.decode()=='SendingEncodings':
                print(f'Client on port {port} is asking to send Encodings')
                file_size=s.recv(1024)
                #m=math.ceil(math.log(int(file_size.decode()),1024))
                s.send('Send'.encode())
                with open('Files/Encodings','wb') as fp:
                    l=s.recv(1024)
                    while l:
                        fp.write(l)
                        l=s.recv(1024)

                s.close()
            
            if received.decode()=='GiveUser':
                if os.path.exists('Files/Client_Auth'):
                    print(f'Client on port {port} is asking to receive User Authentication Data')
                    file_size=str(os.path.getsize('Files/Client_Auth')).encode()
                    s.send(file_size)
                    received1=s.recv(1024)
                    if received1.decode()=='Send':
                        with open('Files/Client_Auth','rb') as fp:
                            l=fp.read(1024)
                            while l:
                                s.send(l)
                                l=fp.read(1024)
                        s.close()
                else:
                    file_size='0'
                    s.send(file_size.encode())
                    s.close()

            elif received.decode()=='SendingUser':
                print(f'Client on port {port} is asking to send User Authentication Data')
                file_size=s.recv(1024)
                s.send('Send'.encode())
                with open('Files/Client_Auth','wb') as fp:
                    l=s.recv(1024)
                    while l:
                        fp.write(l)
                        l=s.recv(1024)
                s.close()


serv=Socket_Server()
serv.Thread2()



