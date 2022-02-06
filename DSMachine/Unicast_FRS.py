import socket
import os
import exceptions

from cv2 import exp


def send_image(ip,port,buffer_size,photo_path,DS_ID):
    s=socket.socket()
    try:
        s.connect((ip,port))
        s.send(f"Avaliable? {DS_ID}")
        
        txt=str(s.recv())
        if txt=="Yes!":
            image_size=os.path.getsize(photo_path)
            s.send(f"SIZE {image_size}")
            while(True):
                image_file=open(photo_path,'rb')
                image_file_bits=image_file.read(buffer_size)
                while(image_file_bits):
                    s.send(image_file_bits)
                    image_file_bits=image_file.read(buffer_size)
                image_file.close()
                txt=str(s.recv())
                if txt=="Image received! Contacting UPS!":
                    s.close()
                    break
                elif txt=="Image corrupted! Send again!":
                    continue
            return "Image_Sent"
        elif txt=="Already Here":
            s.close()
            return "Image Sent"
        else:
            raise exceptions.FRSUnreachableException
    except Exception as e:
        print(f"Error is: {e}")
        raise exceptions.FRSUnreachableException



