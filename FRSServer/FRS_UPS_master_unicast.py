import socket
import exceptions
import json

def main(UPS_master_ip,UPS_master_address, JOB_ID,encoded_image, DS_address):
    s=socket.socket()

    try:
        s.connect((UPS_master_ip,UPS_master_address))
        s.sendall(f"Compare {JOB_ID}")
        txt=str(s.recv())
        if txt=="Okay!":
            s.sendall(DS_address)
            txt=str(s.recv())
            if txt=="Give me encodings":
                encoded_string=json.dumps(encoded_image)
                s.sendall(encoded_string)
                txt=str(s.recv())
                if txt=="Thank you":
                    s.close()
        
        s.shutdown()
        


    except Exception as e:
        raise exceptions.UPS_master_down