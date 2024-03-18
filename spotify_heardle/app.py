# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 21:36:53 2022

@author: User
"""

from spotifyHeardle import heardle
from tkinter import *
from PIL import ImageTk,Image
import math
import json

class App(heardle):
    
    def __init__(self):
        heardle.__init__(self)
        self.playlistIDs = []
        self.playlistNames = []
        self.levelDuration = [1, 2, 4, 6, 10, 17]
        #%% GUI setup
        bgcolor = '#212730'
        root = Tk()
        sx = 1000
        sy = 800    
        ox = math.floor((2560-sx)/2)
        oy = math.floor((1080-sy)/2)
        root.geometry(str(sx)+'x'+str(sy)+'+'+str(ox)+'+'+str(oy))
        root.overrideredirect(True)           
        root.configure(bg=bgcolor)
        
        #%%
        root.bind('<Escape>',self.stop)
        #%%
        
        playlistFrame = Frame(root,bd=2,relief='solid',bg=bgcolor)
        playlistFrame.place(relx =0, rely= 0,width = 0.3*sx,height = sy)

        playlistBox = Listbox(playlistFrame,selectmode = EXTENDED,bg = bgcolor,fg = 'white',font = ("Courier",10)
                    ,relief = FLAT,borderwidth=0, highlightthickness=0)
        playlistBox.place(relx = 0.5,rely = 0,anchor = N,height = 0.75*sy, width = 0.29*sx)
        
        scrollbar = Scrollbar(playlistFrame)
        scrollbar.place(relx = 0.97,rely = 0, anchor = N, height = 0.75*sy)
        scrollbar.config(command = playlistBox.yview)
        
        playlistChooseBtn = generateButton(playlistFrame, bgcolor, "Choose Playlists", self.choosePlaylists)
        playlistChooseBtn.place(relx = 0.5,rely = 0.8,anchor=CENTER)
        
        playlistAddBtn = generateButton(playlistFrame,bgcolor, "Add Playlist To DataBase",self.addPlaylistToDB)
        playlistAddBtn.place(relx = 0.5,rely = 0.95,anchor=CENTER)
        playlistAddTextBox = Text(playlistFrame,height = 1,width = 30,bg = bgcolor, fg = 'white')
        playlistAddTextBox.place(relx = 0.5, rely= 0.9, anchor=CENTER)
        
        
        heardleFrame = Frame(root,bd = 2,relief='solid',bg = bgcolor)
        heardleFrame.place(relx = 0.3, rely = 0, width = 0.7*sx,height = sy)
        
        playImage = PhotoImage(file = 'play.PNG')
        playTrackBtn = generateButton(heardleFrame,bgcolor,'',self.playTrack,image=playImage,bd=0,relief=SUNKEN)
        playTrackBtn.image = playImage
        playTrackBtn.place(relx = 0.5,rely = 0.8,anchor = CENTER)

        playAgainBtn = generateButton(heardleFrame,bgcolor,'Play Again',self.randomizeTrack)
        playAgainBtn.place(relx = 0.1,rely = 0.1,anchor = CENTER)       
        
        skipBtn = generateButton(heardleFrame,bgcolor,'Skip',self.skipLevel)
        skipBtn.place(relx = 0.3,rely = 0.8,anchor = CENTER)
        
        submitBtn = generateButton(heardleFrame,bgcolor,'Submit',self.submitGuess)
        submitBtn.place(relx = 0.8,rely = 0.8,anchor = CENTER)
        
        
        resultLabel = Label(heardleFrame,bg=bgcolor,font = ("Courier",15),text = '',fg = 'White')
        resultLabel.place(relx = 0.5,rely = 0.2,anchor = CENTER)
        
        trackString = StringVar()
        trackString.trace_add('write',self.searchTrack)
        guessTrackTextBox = Entry(heardleFrame,bg = bgcolor, fg = 'white',textvariable = trackString)
        guessTrackTextBox.place(relx =0.5, rely = 0.7,height = 20,width = 400,anchor = CENTER)
        
        guessTrackListBox = Listbox(heardleFrame,bg = bgcolor,fg = 'white',font = ("Courier",10)
                    ,relief = FLAT,borderwidth=0, highlightthickness=0)
        guessTrackListBox.place(relx = 0.5,rely = 0.69,anchor=S,height = 200,width = 400)
        
        guessTrackListBox.bind('<Double-Button>', self.selectTrackFromList)

        
        guessTrackTextBox.bind('<Up>',self.incrementTrackList)
        guessTrackTextBox.bind('<Down>',self.decrementTrackList)
        guessTrackTextBox.bind('<Return>',self.selectTrackFromList)
        guessTrackTextBox.bind('<Control-Return>',self.submitGuess)
        guessTrackTextBox.bind('<Alt-Return>',self.randomizeTrack)
        guessTrackTextBox.bind('<Shift-Return>',self.playTrack)
        guessTrackTextBox.bind('<Shift-Tab>',self.skipLevel)
        
        
        self.playlistBox = playlistBox
        self.playlistFrame = playlistFrame
        self.playlistAddTextBox = playlistAddTextBox
        self.playTrackBtn = playTrackBtn
        self.resultLabel = resultLabel
        self.guessTrackTextBox = guessTrackTextBox
        self.trackString = trackString
        self.guessTrackListBox = guessTrackListBox
        self.root = root
        
        
        self.loadPlaylists()
    def run(self):
        self.root.mainloop()
        
    def stop(self,key):
        self.root.destroy()
        
    def choosePlaylists(self):
        activePlaylists = self.playlistBox.curselection()
        self.reset_tracks()
        print(activePlaylists)
        for playlistIndex in activePlaylists:
            self.add_playlist(self.playlistIDs[playlistIndex])
            
        self.randomizeTrack()
        
        
    def loadPlaylists(self):
        file = open("playlists.json","r")
        self.jsonCont = json.load(file)
        file.close()
        for playlistID in self.jsonCont:
            self.addPlaylistToList(playlistID)
            
    def addPlaylistToDB(self):
        playlistID = self.playlistAddTextBox.get("1.0",END)[:-1]
        playlistID = playlistID.replace('https://open.spotify.com/playlist/','')
        playlistID = playlistID[:playlistID.find('?')]
        if(playlistID not in self.playlistIDs):
            playlistName = self.get_playlist_name(playlistID)
            if(playlistName != None):
                self.jsonCont[playlistID] = playlistName #add new playlist id and name to json content
                file = open("playlists.json","w")
                json.dump(self.jsonCont,file) #save the json content in file
                file.close()
                self.addPlaylistToList(playlistID)
        
    def addPlaylistToList(self,playlistID):
        self.playlistIDs.append(playlistID)
        self.playlistNames.append(self.jsonCont[playlistID])
        self.playlistBox.insert(END,self.jsonCont[playlistID])
        
    def playTrack(self,*args):
        self.play_chosen_track(self.duration)
        
        
        
    def randomizeTrack(self,*args):
        self.pick_track()
        self.level = 1
        self.duration = self.levelDuration[self.level-1]
        self.resultLabel.config(text='')
        self.trackString.set('')
        
        
    def skipLevel(self,*args):
        self.level +=1
        if(self.level <= len(self.levelDuration)):
            self.duration = self.levelDuration[self.level-1]
        else:
            self.resultLabel.config(text=('Failed\n' + 'Correct Answer : ' + self.chosenTrackName))
            
    def submitGuess(self,*args):
        trackAnswer = self.trackString.get()
        if(trackAnswer == self.chosenTrackName):
            self.resultLabel.config(text = 'Correct!')
        else:
            self.resultLabel.config(text=('Failed\n' + 'Correct Answer : ' + self.chosenTrackName))
            
    def searchTrack(self,var,index,mode):
        trackText = self.trackString.get()
        optionalTracks = self.search_track(str(trackText))
        self.guessTrackListBox.delete(0,self.guessTrackListBox.size()-1)
        for i in range(len(optionalTracks)):
            self.guessTrackListBox.insert(END,optionalTracks[i])
                    
        
        
    def incrementTrackList(self,key):
        self.updateHighlightedTrack(-1)
            
    def decrementTrackList(self,key):
        self.updateHighlightedTrack(1)
        
        
    def updateHighlightedTrack(self,offset):
        selectedTrackInd = self.guessTrackListBox.curselection()
        if(len(selectedTrackInd) == 0):
            self.guessTrackListBox.selection_set(0)
        else:
            newInd = selectedTrackInd[0] + offset
            newInd%=self.guessTrackListBox.size()
            self.guessTrackListBox.select_clear(0, "end")
            self.guessTrackListBox.selection_set(newInd)
        
        
    def selectTrackFromList(self,key):
        selectedTrackInd = self.guessTrackListBox.curselection()
        if(len(selectedTrackInd) == 1):
            trackName = self.guessTrackListBox.get(selectedTrackInd[0])
            self.trackString.set(trackName)
            
            

            
        
        
        

def generateCheckButton(master,color,string,var,**kwargs):
    return Checkbutton(master,text=string,variable = var, bg = color, activebackground = color
                       ,font = ("Courier",20),**kwargs)
def generateButton(master,color,string,callback, **kwargs):
    return Button(master,text=string,bg = color,activebackground = color,fg = 'white',command = callback,**kwargs)
        

if __name__ == "__main__":
    app = App()
    app.run()