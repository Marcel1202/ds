import socket 
from threading import Thread
from common.discovery import DiscoveryServerThread
import DS_AS_UNICAST_SERVER as DS_AS

task_list=[[],[]]
# task_list=[[Job ID's ],[[user,pass],...]]
UPS_IP=None

# Multithreaded Python server : TCP Server Socket Thread Pool
class DS_conn(Thread): 
    def __init__(self,ip,port,conn): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        self.conn=conn
        print(f"[+] New server socket thread started for {ip} :{str(port)}") 
 
    def run(self): 
        global task_list
        DSM=DS_AS(task_list)
        flag1,task_list,JOB_ID,username,password=DSM.main(self.conn,self.ip,self.port)
        if flag1=="User Data received":
            pass
            #Here we talk to UPS 
        else:
            pass
        

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 0
BUFFER_SIZE = 1024  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

# Start discovery thread
discovery = DiscoveryServerThread(TCP_IP, 27464, tcpServer.getsockname()[1])
discovery.start()
 
while True: 
    tcpServer.listen(4) 
    print("Multithreaded Python server : Waiting for connections from TCP clients...") 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = DS_conn(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 