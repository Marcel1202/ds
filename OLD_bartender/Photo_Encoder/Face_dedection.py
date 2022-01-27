import cv2
from PIL import Image
import os
import glob
import pickle
import face_recognition as fr
import re
import stdiomask
from PESocket import Photo_Encoder_Socket

class FaceRegistration():
    def __init__(self,name=None,password=None): #Get username and password for needed for our registration 
        if os.path.basename(os.getcwd())=='Project':
            os.chdir('Photo_Encoder')
        if name==None:
            self.name=input("Please input your name/username:")
            self.password=stdiomask.getpass()
            sock=Photo_Encoder_Socket()
            user_list,password_list=sock.ask_for_user_file()
            #Here I get the username/password files and check if the user exists
            #if not exists append to it and send. 

            if self.name not in user_list:
                user_list.append(self.name)
                password_list.append(self.password)
                sock=Photo_Encoder_Socket()
                sock.send_user_file(user_list,password_list)

        else:
            self.name=name
            self.password=password
        self.vid=cv2.VideoCapture(0)
        cascPath='haarcascade_frontalface_default.xml'
        self.faceCascade=cv2.CascadeClassifier(cascPath)     #face cascade used for dedecting a face in the picute 
        #this adds an extra layer of better recognition from our software

    def learn_faces(self):
        os.chdir(r'E:\Classes Infotech\2nd Semester\IOT SMART CITIES\Project\Photo_Encoder')
        os.chdir(r'{}'.format(self.name))

        images_names=glob.glob("*.png")
        
        face_encodings_list=[]
        encoded_images_list=[]
        if os.path.exists(self.name+'_encoded_images'):
            with(open(self.name+'_encoded_images','rb')) as fp:
                encoded_images_list=pickle.load(fp)
            images_names=[image for image in images_names if image not in encoded_images_list]
        

        for image in images_names:
            ftimage=fr.load_image_file(image)
            if len(fr.api.face_encodings(ftimage))!=0:
                face_encodings_list.append(fr.api.face_encodings(ftimage)[0])

        sock=Photo_Encoder_Socket()
        encodings=sock.ask_for_endcodings_file()

        if encodings==0:
            encodings={}
            encodings[self.name]=face_encodings_list
            sock=Photo_Encoder_Socket()
            sock.send_encodings_file(encodings)
        
        else:
            if self.name in encodings:
                encodings[self.name].extend(face_encodings_list)
            else:
                encodings[self.name]=face_encodings_list
            sock=Photo_Encoder_Socket()
            sock.send_encodings_file(encodings)

        encoded_images_list.extend(images_names)
        with open(self.name+'_encoded_images','wb') as fp:
                pickle.dump(encoded_images_list,fp)


    def take_face_photos(self):
        folder_name=r'{}'.format(self.name)

        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        os.chdir(folder_name)

        image_file_list=glob.glob('*.png')
        if len(image_file_list)!=0:
            max1=0
            p=0
            for el in image_file_list:
                j=int(re.search('_(.+?).png',image_file_list[p]).group(1))
                if j>max1:
                    max1=j
                p+=1      
            j=max1
        else:
            j=0

        i=j

        while i<100+j:
            self.ret,frame=self.vid.read()
            cv2.imshow('Frame',frame)
            cv2.waitKey(1)

            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            self.faces=self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE)

            for (x,y,w,h) in self.faces:
                cropped_face_numpy=gray[y:y+h,x:x+w]
                cropped_face=Image.fromarray(cropped_face_numpy)
                cropped_face.save("Face_"+str(i)+".png")
                i+=1

        os.chdir('..')
        self.vid.release()
        cv2.destroyAllWindows()
                

Face=FaceRegistration()
Face.take_face_photos()
Face.learn_faces()
