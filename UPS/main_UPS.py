

from threading import Thread
import socket
import Unicast.FRS_UPS 
import coordination as coord


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
