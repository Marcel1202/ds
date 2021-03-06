import os

class DS_FRS_unicast_Server():
    def __init__(self,buffer_size,task_list):
        pass
        self.buffer_size=buffer_size
        self.task_list=task_list

    def main(self,conn):

        while(True):
            data=conn.recv(self.buffer_size)
            print(f"Received: {data}")
            txt=str(data)


            if txt.startswith("Avaliable?"):

                JOB_ID=txt.split()[1]
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
                image=open(f"temp_{JOB_ID}.png",'wb')
                image_bits=conn.recv(self.buffer_size)
                while(image_bits):
                    image.write(image_bits)
                    image_bits=conn.recv(self.buffer_size)
                image.close()
                local_image_size=os.path.getsize("temp_{JOB_ID}.png")
                if local_image_size==self.image_size:
                    conn.send("Image received! Contacting UPS!")
                    conn.close()
                    break
                else:
                    conn.send("Image corrupted! Send again!")
                    continue
        self.task_list.append(JOB_ID)

        return "Image received", self.task_list, JOB_ID              





