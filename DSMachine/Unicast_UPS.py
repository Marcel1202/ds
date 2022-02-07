import socket
from xml.dom import UserDataHandler
import exceptions


def wait(wait_port,wait_ip):
    print("Waiting for UPS")
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((wait_ip, wait_port))
    tcpServer.listen(1)
    tcpServer.settimeout(60)
    try:
        conn,ip=tcpServer.accept()

        txt=str(conn.recv())
        JOB_ID=txt.split()[1]

        if txt.split()[0]=="Ready":
            conn.send("Yes!")
            txt=str(conn.recv())

            if txt=="0":
                return 0
            else:
                username=txt.split()[1]
                conn.send("Okay!")
                txt=str(conn.recv())
                drink=txt.split()[1]
                conn.send("Thank you! Bye!")
                conn.close()
        
        conn.shutdown()
        return username,drink
    
    except Exception as e:
        print(f"Error: {e}")
        conn.close()
        conn.shutdown()
        raise exceptions.UPS_Timeout







