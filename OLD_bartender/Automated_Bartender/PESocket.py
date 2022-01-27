from pickle import encode_long
import socket
import math
import os
import tempfile
import pickle

class Automated_Bartender_Socket: #communicate Server with Automated Bartender
    def __init__(self):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def ask_for_endcodings_file(self):
        self.s.connect(('localhost',8001))
        self.s.send('GiveEncodings'.encode())
        file_size=self.s.recv(1024)

        if file_size.decode()=='0':
            return 0
        else:
            m=math.ceil(math.log(int(file_size.decode()),1024))
            fd,path=tempfile.mkstemp()
            try:
                with os.fdopen(fd,'wb') as tmp:
                    self.s.send('Send'.encode())
                    l=self.s.recv(1024)
                    while l:
                        tmp.write(l)
                        l=self.s.recv(1024)
            
                with open(path,'rb') as tmp:
                    encodings=pickle.load(tmp)
            finally:
                os.remove(path)

            self.s.close()
            return encodings

    def send_encodings_file(self,encodings): #Not really needed 
        self.s.connect(('localhost',8001))
        self.s.send('SendEncodings'.encode())
        
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
                    self.s.close()
        finally:
            os.remove(path)



#########################################################
    def ask_for_user_dictionary(self):
        self.s.connect(('localhost',8001))
        self.s.send('GiveUserDictionary'.encode())
        file_size=self.s.recv(1024)

        if file_size.decode()=='0':
            return 0
        else:
            m=math.ceil(math.log(int(file_size.decode()),1024))
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
                    user_dict=pickle.load(tmp1)
            finally:
                os.remove(path)

            self.s.close()
            return user_dict

    def send_user_dictionary(self,dict):
        self.s.connect(('localhost',8001))
        self.s.send('SendUserDictionary'.encode())
        
        fd,path=tempfile.mkstemp()

        try:
            with os.fdopen(fd,'wb') as tmp:
                pickle.dump(dict,tmp)
                file_size=str(os.path.getsize(path)).encode()
                self.s.send(file_size)

            with open(path,'rb') as tmp:
                ret=self.s.recv(1024)
                if ret.decode()=='Send':
                    l=tmp.read(1024)
                    while l:
                        self.s.send(l)
                        l=tmp.read(1024)
                    self.s.close() 
        finally:
            os.remove(path)