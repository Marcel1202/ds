import socket
import json
import sys
sys.path.append("..")
import Exceptions.exceptions

def frs(UPS_ip, UPS_addr, JOB_ID,DS_addrs,encoded_image_list):
    s=socket.socket()
    try:
        s.connect((UPS_ip,UPS_addr))
        s.send(f"Job for you {JOB_ID}")

        txt=str(s.recv())
        if txt=="Yes!":
            s.send("Sending address!")
            txt=str(s.recv())
            if txt=="Yes!":
                s.send(str(DS_addrs))
                txt=str(s.recv())
                if txt=="Okay!":
                    s.send("Ready for encodings?")
                    txt=str(s.recv())

                    if txt=="Yes!":
                        encoded_string=json.dumps(encoded_image_list)
                        s.sendall(encoded_string)
                        txt=str(s.recv())
                        if txt=="Received! Comparing and contacting DS on address":
                            s.shutdown()
        
        flag=1
        s.close()
    except Exception as e:
        print(e)
        flag=0
    
    return flag


def As(UPS_ip, UPS_addr, JOB_ID,DS_addrs,user_data):
    s=socket.socket()
    try:
        s.connect((UPS_ip,UPS_addr))
        s.send(f"Job for you {JOB_ID}")

        txt=str(s.recv())
        if txt=="Yes!":
            s.send("Sending address!")
            txt=str(s.recv())
            if txt=="Yes!":
                s.send(str(DS_addrs))
                txt=str(s.recv())
                if txt=="Okay!":
                    s.send("Ready for encodings?")
                    txt=str(s.recv())

                    if txt=="Yes!":
                        user_data_string=json.dumps(user_data)
                        s.sendall(user_data_string)
                        txt=str(s.recv())
                        if txt=="Received! Comparing and contacting DS on address":
                            s.shutdown()
        
        flag=1
        s.close()
    except Exception as e:
        print(e)
        flag=0
    
    return flag