from base64 import encode
import json

class as_ups():
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
            self.conn.send("Give me user data")
            userdata_str=''
            temp=str(self.conn.recv(1024))
            while(temp):
                userdata_str+=temp
                temp=str(self.conn.recv(1024))
            userdata_list=json.loads(userdata_str)
            self.conn.send("Thank you")
            self.conn.close()
        self.conn.shutdown()

        return JOB_ID,addr,userdata_list