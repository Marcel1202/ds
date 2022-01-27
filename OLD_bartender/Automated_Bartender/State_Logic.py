# this file for the states of the automated bartender machine and to show the functionality of it 

import FaceRecognition as FR
import datetime
import keyboard


Fr=FR.FaceRecognition()

# each .run runs the state or the device fully 

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
        to_ret=Fr.camera()
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
        print("State Searching State")
        print('')
        if photo_path==None:
            while True:
                face_dedected=Camera.run()
                if face_dedected==1:
                    break
                else:
                    continue
        face=Fr.find_face_encode_predict(face_photo_path=photo_path)
        drink=None
        hour_now=datetime.datetime.now().hour
        if face==0: #retry again 
            drink=0
        else:
            drink=Fr.get_drink(face,hour_now)
            if drink==None:
                drink=-1

        return face,drink

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

#initializing States
Idle=Idle_Mode() 
Face_Search=Face_Searching()
Face_Recogn=Face_Recognised()
Face_notRecogn=Face_Not_Recognised()

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

    def normal_usage(self): #Automated usage of the Automated Bartender under normal usage. 
        while True:
            motion=Idle.run()
            if motion==0:
                continue
            elif motion==1:
                #next step will be to turn on camera and get frames
                #next one will be to dedect/search face 
                recognised_face,drink=Face_Search.run(photo_path=None) #This is used to run the code on normal operation
                #recognised_face,drink=Face_Search.run(photo_path='Angela_Merkel_0001.jpg') #This part is used to check the output when the user did not register for the Automated bartender.
                #it gives a picture of Angela Merkel to the encoder instead of an image from the camera
                if recognised_face!=0:
                    #next state here will be the Face_recognised where the led 
                    #turn green and the voice approves and says the drink
                    Face_Recogn.run(recognised_face,drink)
                else:
                    #next state in case no face is recognised will be that of 
                    #Face no recognised where the led turns red and the voice
                    # rejects the user
                    Face_notRecogn.run()



Automated_Bart=Automated_Bartender()
Automated_Bart.normal_usage()




