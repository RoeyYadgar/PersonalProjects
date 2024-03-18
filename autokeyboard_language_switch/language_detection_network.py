# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 21:51:25 2022

@author: User
"""

import codecs
import numpy as np
import pandas as pd
import keras
from sklearn import model_selection


#%%


def convertStringToArr(string):
    
    N = 40

    english_letters = 'qwertyuiop[{]}asdfghjkl;:\'"\\zxcvbnm,<.>/? '
    hebrew_letters = '/\'קראטוןםפ]}[{שדגכעיחלךף:,"\\זסבהנמצת>ץ<.? '

    english_trans = [english_letters.find(c.lower()) for c in string[:N]]
    hebrew_trans = [hebrew_letters.find(c.lower()) for c in string[:N]]


    if(english_trans.count(-1) <= hebrew_trans.count(-1)):
        trans = english_trans
    else:
        trans = hebrew_trans
        
    l= len(trans)
    
    if(l < N):
        trans[l:N] = [-2 for i in range(N-l)]


    return trans


def predict_language(string,model):
    prediction = model.predict(convertStringToArr(string))
    
    if(prediction[0][0] > 0.9):
        return 'english'
    elif(prediction[0][1] > 0.9):
        return 'herbew'
    else:
        return 'undecided'


if __name__ == "__main__" : 
    
    #%% Generate Data
    
    fid = codecs.open(r"E:\Downloads\Sentence pairs in Hebrew-English - 2022-07-15.tsv",'r',encoding='utf-8')
    
    text = fid.read()
    text = text.replace('\r','')
    text = text.split('\n')
    text = text[1:-1]
    
    hebrew_text = []
    english_text = []
    
    
    
    for i in range(len(text)):
        t = text[i].split('\t')
        hebrew_text.append(convertStringToArr(t[1]))
        english_text.append(convertStringToArr(t[3]))
    
            
    
    data = np.array(english_text + hebrew_text)
    label =  np.array([[1,0] for i in range(len(english_text))]+ [[0,1] for i in range(len(hebrew_text))])
    pd.DataFrame(data).to_csv("data.csv")
    pd.DataFrame(label).to_csv("label.csv")
    
    
    #%%
    
    
    train_data,test_data,train_label,test_label = model_selection.train_test_split(data,label,test_size = 0.1)
    
    normalizer = keras.layers.Normalization(axis = -1)
    normalizer.adapt(data)
    model = keras.models.Sequential([normalizer,
                                     keras.layers.Dense(100,activation = 'relu'),
                                     keras.layers.Dense(100,activation = 'relu'),
                                     keras.layers.Dense(100,activation = 'relu'),
                                     keras.layers.Dense(2,activation = 'softmax')])
    
    model.compile(loss ='categorical_crossentropy',optimizer = 'adam', metrics=['accuracy'])
    model.fit(train_data,train_label,epochs = 50, batch_size = 100)
    model.evaluate(test_data, test_label)
    #model.save('model')
    
    
