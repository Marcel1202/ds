# this file for the states of the automated bartender machine and to show the functionality of it 

from atexit import register
import datetime
import keyboard
from DSMachine.exceptions import ASUnreachableException
import Unicast_FRS as unicast_FRS
import Unicast_AS as unicast_AS
import Face_dedection as FD
import random

from common.discovery import DiscoveryClient
import exceptions

ip="0.0.0.0" # First Ip we get from broadcast
FRS_port=27525 #First port we get from broadcast



buffer_size=1024

flag_image=False
flag_user_passw=False
counter_FRS=0
counter_AS=0
repeat=None
use_FRS=False
use_AS=False
FRS_ip=None
AS_ip=None

FRS_port=2004
AS_port=2003


class SPEAKER: # these are devices (actuators and sensors that are used) #actuator
    def run(self,name,drink):
        print("Speaker ON")
        if name==-1 and drink==-1:
              print('Face not recognised! Please get assistance at the hotel reception!')  
        elif drink==-1:
            print(f'Speaker: Hello {name}! You have selected no drink. Please log in online to set up the preferred drink for this hour!')
        else:
            print(f'SPEAKER: Hello {name}! Your selected drink is {drink}.')
        print("Speaker OFF")
        print('')

class LED: #Actuator  turns on when face is dedected. 
    def run(self,color):
        print("Led ON")
        print(f'LED: {color}')
        print("Led OFF")
        print('')

class DRINK_MACHINE: #Actuator 
    def run(self,drink):
        print("Drink Machine ON")
        print(f"DRINK MACHINE: Making and delivering {drink}!")
        print("Drink Machine OFF")
        print('')

class DRINK_MACHINE_TAKE_DRINK: #sensor
    def run(self):
        print("Drink Machine Sensor ON")
        keyboard.wait('t')
        print("Drink Taken")
        print('')
        

class CAMERA: #sensor
    def run(self):
        print("Camera ON")
        to_ret=FD.camera()
        print("Camera OFF")
        print('')
        return to_ret

class MOTION_DEDECTOR: #sensor
    def run(self):
        print("Motion Dedector ON")
        keyboard.wait('m')
        print("Motion Dedector OFF")
        print('')
        return 1

class Face_Searching: #state
    def run(self,photo_path=None):
        global flag_image
        print('')
        print("State Searching Face")
        print('')
        if photo_path==None:
            while True:
                face_dedected,photo_path=Camera.run()
                if face_dedected==1:
                    flag_image=True
                    break
                else:
                    continue
        """ face=Fr.find_face_encode_predict(face_photo_path=photo_path)
        drink=None
        hour_now=datetime.datetime.now().hour
        if face==0: #retry again 
            drink=0
        else:
            drink=Fr.get_drink(face,hour_now)
            if drink==None:
                drink=-1 """

        return photo_path

class Face_Recognised: #state
    def run(self,name,drink):
        print('')
        print("Face Recognised State")
        print('')
        Speaker.run(name,drink)
        Led.run('green') 
        if drink!=-1:
            Drink_Machine.run(drink)
            Drink_Machine_Sensor.run()
            
        
class Face_Not_Recognised: #state
    def run(self):
        print('')
        print("Face Not Recognised State")
        print('')
        Led.run('red')
        Speaker.run(-1,-1)
  

class Idle_Mode: #state
    def run(self):
        print('')
        print("Idle State")
        print('')
        mot=Motion_dedector.run() #turn on Motion dedection
        return mot

class Ask_conn_type:
    def run(self,repeat):
        if repeat==None:
            print('Register -> r')
            print("Dedect face and give drink -> d")
            print('Username and password and give drink-> u')
            user_pref=input("Write desiered action and the enter: ")
            return user_pref
        elif repeat=="FRS":
            user_pref=input("FRS connection did not work after 2 tries. Do you want to try an AS connection? (Yes -> y, No-> n)")
            return user_pref
        elif repeat=="AS":
            user_pref=input("AS connection did not work after 2 tries. Do you want to try an FRS connection? (Yes -> y, No-> n)")
            return user_pref

class Unicast_FRS: #state
    def run(self,photo_path,DS_ID):
        print('')
        print("Trying to contact an FRS server")
        print('')
        status=unicast_FRS.send_image(FRS_ip,FRS_port,buffer_size,photo_path,DS_ID)
        return status

class Unicast_AS: #state
    def run(self,user,passw,DS_ID):
        print('')
        print("Trying to contact an AS server")
        print('')
        status=unicast_AS.send_user_data(AS_ip,AS_port,buffer_size,[user,passw],DS_ID)
        return status

class Unicast_wait_UPS:
    def run(self):
        print('')
        print("Waiting for UPS reply")
        print('')
        user_name,drink=unicast_UPS()
        return user_name, drink

#initializing States
Idle=Idle_Mode() 
Face_Search=Face_Searching()
Face_Recogn=Face_Recognised()
Face_notRecogn=Face_Not_Recognised()
Unicast_Frs=Unicast_FRS()
Unicast_As=Unicast_AS()
Unicast_wait_Ups=Unicast_wait_UPS()
conn_type=Ask_conn_type()

#initializing devices
Led=LED()
Speaker=SPEAKER()
Camera=CAMERA()
Motion_dedector=MOTION_DEDECTOR()
Drink_Machine=DRINK_MACHINE()
Drink_Machine_Sensor=DRINK_MACHINE_TAKE_DRINK()



class Automated_Bartender():
    def __init__(self):
        self.unique_ID=f"DS_{random.randint(10,50)}"
        pass

    def face_dedect(self):
        global flag_image
        #Next step here is that we use UNICAST to talk to the FRS server. 
        if flag_image==True:
            photo_path=Face_Search.run(photo_path=1)
        else:
            photo_path=Face_Search.run(photo_path=1)
        status=Unicast_Frs.run(photo_path,self.unique_ID)
        while(True):
            if status==True:
                    #Here we wait and accept Unicast from one of the UPS servers 
                [user_name,drink]=Unicast_wait_Ups.run()
                        #unicast_wait_UPS should contain in a list [person name, drink]
                if user_name==None:
                    break

        return user_name,drink

    def user_pass(self):
        user=input("Please input your userame: ")
        passw=input("Please input your password: ")
        while(True):
            status=Unicast_As.run(user,passw,self.unique_ID)
            if status==True:
                    #Here we wait and accept Unicast from one of the UPS servers 
                [user_name,drink]=Unicast_wait_Ups.run()
                        #unicast_wait_UPS should contain in a list [person name, drink]
                if user_name==None:
                    continue
                else:
                    break
            else:
                pass
                user_name=None
                drink=None
                break
        
        return user_name,drink


    def normal_usage(self): #Automated usage of the Automated Bartender under normal usage. 
        global repeat
        global use_AS
        global use_FRS
        global regis
        
        while True:
            motion=Idle.run()
            if motion==0:
                continue
            elif motion==1:
                while(True):
                    if use_AS==False and use_FRS==False:
                        conn=conn_type.run(repeat)
                        if conn=='d':
                            use_FRS=True
                        elif conn=='u':
                            use_AS=True
                    if use_FRS==True:
                        [user_name,drink]=self.face_dedect()
                        break
                    elif use_AS==True:
                        [user_name,drink]=self.user_pass()
                        break
                    else:
                        print("Wrong input! Try again!")
    
                if user_name!=0:
                    #next state here will be the Face_recognised where the led 
                    #turn green and the voice approves and says the drink
                    Face_Recogn.run(user_name,drink)
                else:
                    #next state in case no face is recognised will be that of 
                    #Face no recognised where the led turns red and the voice
                    # rejects the user
                    Face_notRecogn.run()


# Discover FRS and AS Server
while True:
    try:
        discovery = DiscoveryClient("", 27463)
        FRS_ip=discovery.discover()
        print("FRS IP:", FRS_ip)

        discovery = DiscoveryClient("", 27464)
        AS_ip=discovery.discover()
        print("AS IP:", AS_ip)

        Automated_Bart = Automated_Bartender()
        Automated_Bart.normal_usage()
    except exceptions.FRSUnreachableException:
        print("A FRS has become unreachable. Broadcasting again")
        counter_FRS+=1
        if counter_FRS>2:
            repeat="FRS"
            use_FRS=False
    except exceptions.ASUnreachableException:
        print("A AS has become unreachable. Broadcasting again")
        counter_AS+=1
        if counter_FRS>2:
            repeat="AS"
            use_AS=False

    except exceptions.UPSTimeOut:
        print("UPS Server is taking too long to reply! Contacting again")