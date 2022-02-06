import socket
import os
import exceptions

from cv2 import exp


def send_user_data(ip,port,buffer_size,user_data,DS_ID):
    s=socket.socket()
    try:
        s.connect((ip,port))
        s.send(f"Avaliable? {DS_ID}")
        
        txt=str(s.recv())
        if txt=="Yes!":
            s.send(str(user_data[0]))
            txt=str(s.recv())
            if txt=='Username OK':
                s.send(str(user_data[1]))
                txt=str(s.recv())
                if txt=='Passw OK! Contacting UPS!':
                    s.close()
                    print("Username and Password sent")
            return "Data_Sent"
        elif "Already here":
            s.close()
            return "Data_Sent"
        else:
            raise exceptions.FRSUnreachableException
    except Exception as e:
        print(f"Error is: {e}")
        raise exceptions.FRSUnreachableException