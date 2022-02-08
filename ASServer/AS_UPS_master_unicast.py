import socket
import exceptions
import json

def main(UPS_master_ip,UPS_master_address, JOB_ID,user_data, DS_address):
    s=socket.socket()

    try:
        s.connect((UPS_master_ip,UPS_master_address))
        s.sendall(f"Compare {JOB_ID}")
        txt=str(s.recv())
        if txt=="Okay!":
            s.sendall(DS_address)
            txt=str(s.recv())
            if txt=="Give me user data":
                user_string=json.dumps(user_data)
                s.sendall(user_string)
                txt=str(s.recv())
                if txt=="Thank you":
                    s.close()
        
        s.shutdown()
        
    except Exception as e:
        raise exceptions.UPS_master_down