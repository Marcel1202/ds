import socket
from threading import Thread
import DS_FRS_UNICAST_SERVER as DS_FRS
import Face_encoder as Fe

# Multithreaded Python server : TCP Server Socket Thread Pool
from common.discovery import DiscoveryServerThread

task_list=[]
UPS_IP=None

class DS_conn(Thread):
    def __init__(self,ip,port,conn,BUFFER_SIZE):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn=conn
        self.BUFFER_SIZE=BUFFER_SIZE
        self.FE=Fe()
        print(f"[+] New server socket thread started for {ip} :{str(port)}")

    def run(self):
        global task_list
        DSM=DS_FRS(self.BUFFER_SIZE,task_list)
        flag1,task_list,JOB_ID=DSM.main(self.conn,self.ip,self.port)
        if flag1=='Image received':
            self.encoded_image=self.FE.encode_face(f'temp_{JOB_ID}.png')
        else:
            pass
        if self.encoded_image!=None:
            pass
            #Send image to UPS after contacting (Semd encodeded image and the ip of the DS machine)
        else:
            pass


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 0
BUFFER_SIZE = 1024

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

# Start discovery thread
discovery = DiscoveryServerThread(TCP_IP, 27463, tcpServer.getsockname()[1])
discovery.start()

while True: 
    tcpServer.listen(4) 
    print("Multithreaded Python server : Waiting for connections from TCP clients...") 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = DS_conn(ip,port,conn,BUFFER_SIZE) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 