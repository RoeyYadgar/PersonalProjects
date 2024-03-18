# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 18:08:15 2021

@author: User
"""

from tkinter import *
from PIL import ImageTk, Image
import threading
import math
import json
import socket
import socket_comm

class App():
    def __init__(self):
        
        #%% client setup
        port = 5050
        server = socket.gethostbyname(socket.gethostname())
        addr = (server,port)
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(addr)
        self.json = json.loads(socket_comm.read(self.client))
        
        #%% GUI setup
        bgcolor = '#212730'
        root = Tk()
        sx = 300
        sy = 300    
        ox = math.floor((2560-sx)/2)
        oy = math.floor((1080-sy)/2)
        root.geometry(str(sx)+'x'+str(sy)+'+'+str(ox)+'+'+str(oy))
        root.overrideredirect(True)           
        root.configure(bg=bgcolor)
        
        #%% Key binds
        root.bind('<Escape>', self.stop)
        root.bind('<Up>',self.incrementTemp)
        root.bind('w',self.incrementTemp)
        root.bind('<Down>',self.decrementTemp)
        root.bind('s',self.decrementTemp)
        root.bind('<Right>',self.incrementFan)
        root.bind('d',self.incrementFan)
        root.bind('<Left>',self.decrementFan)
        root.bind('a',self.decrementFan)
        root.bind('<Tab>',self.cycleMode)
        root.bind('<space>',self.toggleState)
        root.bind('<Return>',self.sendJsonData)
        root.bind('<Button-1>',self.mouseClick)
        #%% Temprature widgets
        tempFrame = Frame(root,bd=3,relief='solid',bg=bgcolor)
        tempLabel = Label(tempFrame, font=("Courier",50),bg=bgcolor)        
        tempLabel.place(relx = 0.5, rely =0.5,anchor = CENTER)
        
        #%% Fan widgets
        fanFrame = Frame(root,bd =3, relief = 'solid',bg=bgcolor)
        fanLabel = Label(fanFrame,font=("Courier",20),bg = bgcolor,text ='FAN')
        fanLabel.place(relx = 0.2, rely = 0.575, anchor = CENTER)
        fanImg = Label(fanFrame,width = 100, height = 50,bg = bgcolor)
        fanImg.place(relx = 0.7,rely = 0.4, anchor = CENTER)
        self.fanImages = {'Auto' : load_img('images/fanauto.png',(140,70))
                          ,'1' : load_img('images/fan1.png',(140,70)) 
                          ,'2' : load_img('images/fan2.png',(140,70))
                          , '3':load_img('images/fan3.png',(140,70))}
        
        
        #%% Mode Widgets
        modeFrame = Frame(root,bd=3,relief='solid',bg = bgcolor)
        modeImg = {'Auto': Label(modeFrame,bg = bgcolor),
                   'Cool': Label(modeFrame,bg = bgcolor),
                   'Dry': Label(modeFrame,bg = bgcolor),
                   'Fan': Label(modeFrame,bg = bgcolor),
                   'Heat': Label(modeFrame,bg = bgcolor)}
        for (i,key) in zip(range(len(modeImg)),modeImg):
            modeImg[key].place(relx = 0.5,rely = 0.1 + 0.2*i,anchor=CENTER)
        
        
        #%% On/Off Widgets
        stateFrame = Frame(root,bd=3,relief='solid',bg = bgcolor)
        stateImg = Label(stateFrame,bg = bgcolor)
        stateImg.place(relx = 0.75,rely = 0.5,anchor=CENTER)
        self.stateImages = {'on' : load_img('images/onswitch.png',(112,50))
                            ,'off':load_img('images/offswitch.png',(112,50))}
        


        #%% Frame Placement
        fanFrame.place(relx =0.25, rely = 0, width = 0.75*sx,height=0.25*sy)
        tempFrame.place(relx =0.25, rely= 0.25,width = 0.75*sx,height = 0.55*sy)
        modeFrame.place(relx = 0, rely = 0, width = 0.25*sx,height = 0.8*sy)
        stateFrame.place(relx=0,rely = 0.8, width = sx, height = 0.2*sy)
        #%% Assiging widgets to object
        self.root = root
        
        self.tempFrame = tempFrame
        self.tempLabel = tempLabel
        
        self.fanFrame = fanFrame
        self.fanImg = fanImg
        
        self.modeFrame = modeFrame
        self.modeImg = modeImg
        
        self.stateFrame = stateFrame
        self.stateImg = stateImg
        
        #%% display Initalized data
        self.updateTemp()
        self.updateFan()
        self.loadMode()
        self.updateMode()
        self.updateState()
        
        
        
    #%% Object Functions
    def run(self):
        self.root.mainloop()
        
    def stop(self,key):
        self.root.destroy()
        socket_comm.send(self.client,"close")
        
    
    def incrementTemp(self,key):
        self.json['Temperature']+=1
        self.updateTemp()
        
    def decrementTemp(self,key):
        self.json['Temperature']-=1
        self.updateTemp()
        
        
    def incrementFan(self,key):
        fanKeys = list(self.fanImages)
        self.json['Fan Speed'] = fanKeys[(fanKeys.index(self.json['Fan Speed']) + 1)%(len(fanKeys))]
        self.updateFan()
    
    def decrementFan(self,key):
        fanKeys = list(self.fanImages)
        self.json['Fan Speed'] = fanKeys[(fanKeys.index(self.json['Fan Speed']) - 1)%(len(fanKeys))]
        self.updateFan()
        
        
    def cycleMode(self,key):
        modeKeys = list(self.modeImg)
        self.json['Mode'] = modeKeys[(modeKeys.index(self.json['Mode']) + 1)%(len(modeKeys))]
        self.updateMode()
        
    def toggleState(self,key):
        stateKeys = list(self.stateImages)
        self.json['State'] = stateKeys[(stateKeys.index(self.json['State']) + 1)%(len(stateKeys))]
        self.updateState()
        
    def updateTemp(self):
        self.tempLabel.config(text=str(self.json['Temperature']))

    
    def updateFan(self):
        self.fanImg.image = self.fanImages[self.json['Fan Speed']]
        self.fanImg['image'] = self.fanImg.image
        
    def updateMode(self):
        for key in self.modeImg:
            self.modeImg[key]['image'] = ''
            
        self.modeImg[self.json['Mode']]['image'] = self.modeImg[self.json['Mode']].image
        
    def loadMode(self):
        for key in self.modeImg:
            #img = Image.open('images/'+key+'.png')
            #img = ImageTk.PhotoImage(img.resize((40,40)))
            img = load_img('images/'+key+'.png',(40,40))
            self.modeImg[key].image = img
            self.modeImg[key]['image'] = self.modeImg[key].image
            
            
            
    def updateState(self):
        self.stateImg.image = self.stateImages[self.json['State']]
        self.stateImg['image'] = self.stateImg.image
        

    def sendJsonData(self,key):
        socket_comm.send(self.client,json.dumps(self.json))
        
        
    def mouseClick(self,event):
        wid = event.widget
        if(wid == self.fanFrame or wid in self.fanFrame.winfo_children()):
            self.incrementFan(None)
        if(wid == self.modeFrame or wid in self.modeFrame.winfo_children()):
            self.cycleMode(None)
        if(wid == self.stateFrame or wid in self.stateFrame.winfo_children()):
            self.toggleState(None)
        
    
def load_img(path,size):
    full_path = 'E:\\miscellaneous\\ACremote\\'
    img = Image.open(full_path+path)
    img = ImageTk.PhotoImage(img.resize(size))    
    return img
  
      
            
if __name__ == "__main__":
    app = App()
    app.run()

    
