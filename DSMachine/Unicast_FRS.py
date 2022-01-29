import socket
import os


def send_image(ip,port,buffer_size,photo_path):
    s=socket.socket()

    s.connect((ip,port))
    s.send("Avaliable?")
    
    txt=str(s.recv())
    if txt=="Yes!":
        image_size=os.path.getsize(photo_path)
        s.send(str(image_size))
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
    else:
        pass


