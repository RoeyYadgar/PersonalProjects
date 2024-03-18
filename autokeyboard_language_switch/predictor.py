# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 22:58:36 2022

@author: User
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import keras
#from language_detection_network import predict_language
from pathlib import Path
import sys
import numpy as np
from language_funcs import convertArrToString,convertStringToArr

def predict_language(string,model):
    arr = convertStringToArr(string)
    prediction = model.predict(arr,verbose = 0)
    
    
    english_letters = 'qwertyuiop[{]}asdfghjkl;:\'"\\zxcvbnm,<.>/? '
    hebrew_letters = '/\'קראטוןםפ]}[{שדגכעיחלךף:,"\\זסבהנמצת>ץ<.? '
    
    if(prediction[0][0] > 0.97): #Model predicts english
        letters = english_letters
    elif(prediction[0][1] > 0.97): #Model predicts hebrew
        letters = hebrew_letters
    else:
        return string
    
    
    return convertArrToString(arr[0],letters,string)
    
    

model = keras.models.load_model(Path(__file__).parent / 'model2')


while(True):

    string = sys.stdin.readline().replace('\n', '')
    
    string = bytes.fromhex(string).decode("utf-16")[:-1]


    output = (predict_language(string, model))
    
    
    sys.stdout.writelines(output.encode("utf-16").hex()[4:]+ "0000" + "\n")
    sys.stdout.flush()
   