

import Unicast.UPS_Master_UPS_slave as unicast_master_slave

UPS_ip='0.0.0.0'

def coordinate(task_dict,JOB_ID,addr,encoded_image_list):
    while(True): 
        min_UPS=list(task_dict.keys())[0]
        min_UPS_task=len(task_dict[list(task_dict.keys())[0]])
        for key,items in task_dict.items():
            if min_UPS_task>len(items):
                min_UPS=key
                min_UPS_task=len(items)
        
        UPS_addr=min_UPS.split()[1]

    
        flag=unicast_master_slave.main(UPS_ip, UPS_addr, JOB_ID, encoded_image_list)

        if flag==1:
            break
        if flag==0: #could not contact the UPS server so server down.
            del task_dict[min_UPS]
            continue
    
    task_dict[min_UPS].append(JOB_ID)

    return task_dict
         

    