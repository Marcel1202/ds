import os

class DS_FRS_unicast_Server():
    def __init__(self,buffer_size,task_list):
        pass
        self.buffer_size=buffer_size
        self.task_list=task_list

    def main(self,conn,ip,port):
        self.ip=ip
        self.port=port

        while(True):
            data=conn.recv(self.buffer_size)
            print(f"Received: {data}")
            txt=str(data).split


            if txt[0]=="Avaliable?":
                JOB_ID=txt[1]
                if JOB_ID not in self.task_list:
                    conn.send("Yes!")
                else:
                    conn.send("Already Here")
                    conn.close()
                    break

            elif txt.startwith("SIZE"):
                image_size=txt.split()[1]
                self.image_size=int(image_size)
            
            elif data:
                image=open("temp.png",'wb')
                image_bits=conn.recv(self.buffer_size)
                while(image_bits):
                    image.write(image_bits)
                    image_bits=conn.recv(self.buffer_size)
                image.close()
                local_image_size=os.path.getsize("temp.png")
                if local_image_size==self.image_size:
                    conn.send("Image received! Contacting UPS!")
                    conn.close()
                    break
                else:
                    conn.send("Image corrupted! Send again!")
                    continue

        return "Image received", self.task_list, JOB_ID              





