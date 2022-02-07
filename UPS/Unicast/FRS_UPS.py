import json

class frs_ups():
    def __init__(self,conn,ip):
        self.conn=conn
        self.ip=ip

    def main(self):
        txt=str(self.conn.recv())

        if txt.split()[0]=="Compare":
            JOB_ID=txt.split()[1]
            self.conn.send("Okay!")
            txt=str(self.conn.recv())
            addr=txt
            self.conn.send("Give me encodings")
            encoded_image=''
            temp=str(self.conn.recv(1024))
            while(temp):
                encoded_image+=temp
                temp=str(self.conn.recv(1024))
            encoded_image_list=json.loads(encoded_image)




