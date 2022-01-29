# this file for the states of the automated bartender machine and to show the functionality of it 

from atexit import register
import datetime
import keyboard
import Unicast_FRS as unicast_FRS

from common.discovery import DiscoveryClient

ip="0.0.0.0" # First Ip we get from broadcast
FRS_port=27525 #First port we get from broadcast



buffer_size=1024



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
        print('')
        print("State Searching Face")
        print('')
        if photo_path==None:
            while True:
                face_dedected,photo_path=Camera.run()
                if face_dedected==1:
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
            print('Username and password -> u')
            user_pref=input("Write desiered action and the enter: ")
            return user_pref
        elif repeat=="FRS":
            user_pref=input("FRS connection did not work after 2 tries. Do you want to try an AS connection? (Yes -> y, No-> n)")
            return user_pref
        elif repeat=="AS":
            user_pref=input("AS connection did not work after 2 tries. Do you want to try an AS connection? (Yes -> y, No-> n)")
            return user_pref

class Unicast_FRS: #state
    def run(self,photo_path):
        print('')
        print("Trying to contact an FRS server")
        print('')
        status=unicast_FRS.send_image(ip,FRS_port,buffer_size,photo_path)
        return status

class Unicast_AS: #state
    def run(self,user,passw):
        print('')
        print("Trying to contact an AS server")
        print('')
        status=unicast_AS(user,passw)
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
        pass

    def face_dedect(self):
        #Next step here is that we use UNICAST to talk to the FRS server. 
        photo_path=Face_Search.run(photo_path=None)
        status=Unicast_Frs.run(photo_path)
        while(True):
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
                #Photo not sent correctly. Retry again 1 more time and next move to AS Server
                #     
                break

        return user_name,drink

    def user_pass(self):
        user=input("Please input your userame: ")
        passw=input("Please input your password: ")
        while(True):
            status=Unicast_As.run(user,passw)
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
        while True:
            motion=Idle.run()
            if motion==0:
                continue
            elif motion==1:
                repeat=None
                while(True):
                    conn=conn_type.run(repeat)
                    if conn=='d':
                        [user_name,drink]=self.face_dedect()
                        if user_name==None:
                            repeat="FRS"
                            continue
                        else:
                            break
                    elif conn=='u':
                        [user_name,drink]=self.user_pass()
                        if user_name==None:
                            repeat="AS"
                            continue
                        else:
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
discovery = DiscoveryClient("", 27463)
print("FRS IP:", discovery.discover())

discovery = DiscoveryClient("", 27464)
print("AS IP:", discovery.discover())

Automated_Bart=Automated_Bartender()
Automated_Bart.normal_usage()




