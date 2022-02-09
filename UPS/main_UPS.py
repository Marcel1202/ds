import time
import random
from threading import Thread
import socket
import Unicast.Master.FRS_UPS
import coordination as coord
from UPS.election import ElectionThread

# Dummy network
from UPS.replication import ReplicationThread
from common.discovery import UPSDiscoveryClient, UPSDiscoveryServerThread

#fake_network = [('127.0.0.1', 4560), ('127.0.0.1', 4561), ('127.0.0.1', 4562), ('127.0.0.1', 4563)]
network = []

IP = "0.0.0.0"
port = random.randrange(1000, 65535)

master_server = UPSDiscoveryClient('0.0.0.0', 27466, port).discover()

ElectionThread.network = network
ElectionThread.IP = IP
ElectionThread.port = port
ElectionThread.leader_IP = master_server[0]
ElectionThread.leader_port = master_server[1]
ElectionThread("receiver").start()

UPSDiscoveryServerThread('0.0.0.0', 27466, port, network).start()
ReplicationThread().start()

# Send Election Request
# ElectionThread("sender", "election").start()

task_dict=dict()
"{'UPS_name address':[task list]}"

class Unicast_FRS_UPS_coord(Thread):
    def __init__(self,ip,conn):
        Thread.__init__(self)
        self.ip=ip
        self.conn=conn
        self.uni_frs=Unicast.FRS_UPS.frs_ups(self.conn,self.ip)

    
    def run(self):
        global task_dict
        JOB_ID,addr,encoded_image_list=self.uni_frs.main()
        task_list=coord.coordinate(task_dict,JOB_ID,addr,encoded_image_list)
