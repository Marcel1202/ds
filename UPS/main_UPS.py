import time
from threading import Thread
import socket
import Unicast.FRS_UPS 
import coordination as coord
from UPS.election import ElectionThread2

fake_network = [('127.0.0.1', 4560), ('127.0.0.1', 4561), ('127.0.0.1', 4562), ('127.0.0.1', 4563)]
port = fake_network[1][1]

ElectionThread2.higher = 0
for address in fake_network:
    if address[1] > port:
        ElectionThread2.higher += 1

ElectionThread2.network = fake_network
ElectionThread2.self_id = port
ElectionThread2("receiver").start()

time.sleep(0)
ElectionThread2("sender", "election").start()

# discovery_client = UPSDiscoveryClient('0.0.0.0', 27466, port)
# master_server = discovery_client.discover()

# network = []
#
# if master_server == ('127.0.0.1', port):
#     UPSDiscoveryServerThread('0.0.0.0', 27466, 0, network).start()


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
