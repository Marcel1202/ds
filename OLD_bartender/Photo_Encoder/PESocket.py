
from genericpath import getsize
from pickle import encode_long
import socket
import math
import os
import tempfile
import pickle

class Photo_Encoder_Socket: #code used to communicate between the file server and photo encoder
    def __init__(self):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def ask_for_endcodings_file(self):
        self.s.connect(('localhost',8002))
        self.s.send('GiveEncodings'.encode())
        file_size=self.s.recv(1024)

        if file_size.decode()=='0':
            return 0 # file not there 
        else:
            fd,path=tempfile.mkstemp()
            try:
                with os.fdopen(fd,'wb') as tmp:
                    self.s.send('Send'.encode())
                    l=self.s.recv(1024)
                    i=0
                    while l:
                        tmp.write(l)
                        l=self.s.recv(1024)
                with open(path,'rb') as tmp1:
                    encodings=pickle.load(tmp1)

            finally:
                os.remove(path)

            self.s.close()
            return encodings

    def send_encodings_file(self,encodings):
        self.s.connect(('localhost',8002))
        self.s.send('SendingEncodings'.encode())
        
        fd,path=tempfile.mkstemp()

        try:
            with os.fdopen(fd,'wb') as tmp:
                pickle.dump(encodings,tmp)
                file_size=str(os.path.getsize(path)).encode()
                self.s.send(file_size)

            with open(path,'rb') as tmp:
                ret=self.s.recv(1024)
                if ret.decode()=='Send':
                    l=tmp.read(1024)
                    while l:
                        self.s.send(l)
                        l=tmp.read(1024)
            
        finally:
            os.remove(path)
        
        self.s.close() 

###############################################    
    def ask_for_user_file(self):
        self.s.connect(('localhost',8002))
        self.s.send('GiveUser'.encode())
        file_size=self.s.recv(1024)

        if file_size.decode()=='0':
            return 0 # file not there 
        else:
            fd,path=tempfile.mkstemp()
            try:
                with os.fdopen(fd,'wb') as tmp:
                    self.s.send('Send'.encode())
                    l=self.s.recv(1024)
                    i=0
                    while l:
                        tmp.write(l)
                        l=self.s.recv(1024)
                with open(path,'rb') as tmp1:
                    user_list,pass_list=pickle.load(tmp1)
            finally:
                os.remove(path)

            self.s.close()
            return user_list,pass_list

    def send_user_file(self,user_list,password_list):
        self.s.connect(('localhost',8002))
        self.s.send('SendingUser'.encode())
        
        fd,path=tempfile.mkstemp()

        try:
            with os.fdopen(fd,'wb') as tmp:
                pickle.dump((user_list,password_list),tmp)
                file_size=str(os.path.getsize(path)).encode()
                self.s.send(file_size)

            with open(path,'rb') as tmp:
                ret=self.s.recv(1024)
                if ret.decode()=='Send':
                    l=tmp.read(1024)
                    while l:
                        self.s.send(l)
                        l=tmp.read(1024)
                 
        finally:
            os.remove(path)
        self.s.close()
        




