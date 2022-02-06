import os

class DS_FRS_unicast_Server():
    def __init__(self,task_list):
        pass
        self.task_list=task_list

    def main(self,conn):

        while(True):
            data=conn.recv(self.buffer_size)
            print(f"Received: {data}")
            txt=str(data).split

            if txt[0]=="Avaliable?":
                JOB_ID=txt[1]
                if JOB_ID not in self.task_list[0]:
                    conn.send("Yes!")
                else:
                    conn.send("Already Here")
                    username=self.task_list[1][self.task_list.index(JOB_ID)][0]
                    password=self.task_list[1][self.task_list.index(JOB_ID)][1]
                    conn.close()
                    break
                
                txt=str(conn.recv())
                username=txt
                conn.send("Username OK")
                txt=str(conn.recv())
                password=txt
                conn.send("Passw OK! Contacting UPS!")
                conn.close()
                self.task_list[0].append(JOB_ID)
                self.task_list[1].append([username,password])
                break

        return "User Data received", self.task_list, JOB_ID, username, password              
          





