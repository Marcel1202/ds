
import cv2
from PIL import Image
import os
import face_recognition as fr
import torch
import numpy as np
from PESocket import Automated_Bartender_Socket


class FileNotFoundErr(Exception):
    pass

class FaceEncoder():
    def __init__(self):
        pass

    def encode_face(self,face_photo_path):      
        cropped_face=fr.load_image_file(face_photo_path)
        encoded_face=fr.api.face_encodings(cropped_face)
        if len(encoded_face) == 0:
            return None
        else:
            return encoded_face

