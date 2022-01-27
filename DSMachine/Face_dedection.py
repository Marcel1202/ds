
import cv2
from PIL import Image
import os
import face_recognition as fr
#import torch
import numpy as np
from PESocket import Automated_Bartender_Socket


class FileNotFoundErr(Exception):
    pass



class FaceDedection():
    def __init__(self):
        #self.device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        #print(os.path.basename(os.getcwd()))
        if os.path.basename(os.getcwd())=='Project':
            os.chdir('DSMachine')

        #self.encodings_dict=None



    """ def get_drink(self,name,time): #finds drink in database if face was found
        sock=Automated_Bartender_Socket()
        user_dictionary=sock.ask_for_user_dictionary()

        hour_list=user_dictionary[name]

        drink=None

        for row in hour_list:
            if (time>=row[1] and time<row[2]):
                drink=row[0]
                break

        return drink """


    """ def compare_encoding_to_database(self,encoded_face): # compares encoded image to database and defines if a face was found or not  
        #Get dictionary
        sock=Automated_Bartender_Socket()
        self.encodings_dict=sock.ask_for_endcodings_file()
        if self.encodings_dict!=0:

            encoded_face_tensor=torch.tensor(encoded_face,device=self.device)

            min_distance_vector=torch.zeros((len(self.encodings_dict.keys()),),device=self.device)

            for i, values in enumerate(self.encodings_dict.values()):
                temp_tensor=torch.tensor(values,device=self.device)
                min_distance_vector[i]=torch.min(torch.sqrt(torch.sum((encoded_face_tensor-temp_tensor)**2,axis=1)))
            min_distance=torch.min(min_distance_vector)
            print(min_distance_vector)
            if min_distance<0.45:
                return list(self.encodings_dict.keys())[torch.argmin(min_distance_vector)]
            else:
                return 0
        else: 
            raise FileNotFoundError """


    def camera(self): #turns on camera and waits for face to be found 
        vid=cv2.VideoCapture(0)
        cascPath='haarcascade_frontalface_default.xml'
        faceCascade=cv2.CascadeClassifier(cv2.data.haarcascades + cascPath)
        every_other=True
        while True:
            if not every_other:
                every_other=not every_other
                continue
            every_other=not every_other

            ret,frame=vid.read()
            
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            y_shape=200
            x_shape=200
            (y_height,x_width)=gray.shape
            gray=gray[int(np.floor(0.5*(y_height-y_shape))):int(np.floor(0.5*(y_height+y_shape))),int(np.floor(0.5*(x_width-x_shape))):int(np.floor(0.5*(x_width+x_shape)))]
            cv2.imshow('Webcam',gray)
            cv2.waitKey(1)

            faces=faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE)
            if len(faces)!=0:
                    max_area=0.0
                    (max_x,max_y,max_w,max_h)=(0.0,0.0,0.0,0.0)

                    for(x,y,w,h) in faces:
                        if max_area<w*h:
                            max_area=w*h
                            (max_x,max_y,max_w,max_h)=(x,y,w,h)
                    
                    cropped_face=gray[max_y:max_y+max_h,max_x:max_x+max_w]
                    cropped_face=Image.fromarray(cropped_face)
                    photo_path='temp_face.png'
                    cropped_face.save(photo_path)
                    print(os.path.exists('temp_face.png'))
                    vid.release()
                    cv2.destroyAllWindows()
                    break
        return 1,photo_path
       
    """ def find_face_encode_predict(self,face_photo_path=None):
        if face_photo_path==None:
            ################Here we send the photo using unicast to the FRS ####################
            #unicast('temp_face.png')
             while True:
                #cropped_face=fr.load_image_file('temp_face.png')
                #os.remove('temp_face.png')
                #encoded_face=fr.api.face_encodings(cropped_face)
                if len(encoded_face) == 0:
                    continue #maybe no face there check next one 
                else:
                    predicted_name=self.compare_encoding_to_database(encoded_face)
                    break 
        else: # give an image path to be dedected rather then using the camera
             
            cropped_face=fr.load_image_file(face_photo_path)
            encoded_face=fr.api.face_encodings(cropped_face)
            if len(encoded_face) == 0:
                #No face 
                predicted_name=0
            else:
                predicted_name=self.compare_encoding_to_database(encoded_face) 
        return predicted_name """

