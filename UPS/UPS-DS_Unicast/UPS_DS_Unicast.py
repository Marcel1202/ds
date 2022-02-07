import socket 
import Exceptions.exceptions as ex


class UPS_DS_Unicast():
    def init(self,ip,port):
        try:
            self.s=socket.socket()
            self.s.connect((ip,port))
        except Exception as e:
            print(e)
            raise ex.DSnotAvaliable

    def main(self,JOB_ID,results):
        self.s.send(f"Ready_{JOB_ID}")
        txt=str(self.s.recv())

        if txt=="Yes!":
            if results==0:
                self.s.send(f"{results}")
            else:
                self.s.send(f"Name {results[0]}")
                txt=str(self.s.recv())
                if txt=="Okay!":
                    self.s.send(f"Drink {results[1]}")
                    txt=str(self.s.recv())
                    if txt=="Thank you! Bye!":
                        self.s.close()


        