# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 22:14:09 2022

@author: User
"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
import vlc
import time
import numpy as np
from random import randint

CLIENTID = None
clientSECRET = None
class heardle():
    
    def __init__(self):
        clientID = CLIENTID
        clientSecret = clientSECRET
        redirectURI = 'http://example.com'
        #spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret))
        self.spotify = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id=clientID,client_secret=clientSecret,redirect_uri=(redirectURI)))
        self.playlistTrackName = []
        self.playlistPreviewURL = []
        
        return 
    def reset_tracks(self):
        self.playlistTrackName = []
        self.playlistPreviewURL = []
        
    
    def add_playlist(self,playlistID):
        
        playlistResponse = self.spotify.playlist(playlistID + '/tracks?offset=0&limit=100&market=ES&additional_types=track')        
        trackNum = playlistResponse['total']
        self.add_tracks(playlistResponse)
        numRequest = int(np.ceil(trackNum/100)) - 1
        trackOffset = 100;
        for i in range(numRequest):
            playlistResponse = self.spotify.playlist(playlistID + '/tracks?offset='+ str(trackOffset) + '&limit=100&market=ES&additional_types=track')        
            self.add_tracks(playlistResponse)
            trackOffset += 100
   
        return 
        
    def add_tracks(self, playlistResponse):
        
        for item in playlistResponse['items']:
            track = item['track']
            
            trackName = track['name'] + ' - '
            for i,artist in enumerate(track['artists']):
                trackName += artist['name']
                if(i < len(track['artists']) - 1):
                    trackName += ' & '
            
            self.playlistTrackName.append(trackName) 
            self.playlistPreviewURL.append(track['preview_url'])
            
        return 
    
    
    
    
    def pick_track(self):
        trackNo = randint(0,len(self.playlistTrackName)-1)
        self.chosenTrackName = self.playlistTrackName[trackNo]
        self.chosenTrackURL = self.playlistPreviewURL[trackNo]
        self.player = vlc.MediaPlayer(self.chosenTrackURL)
        self.player.audio_set_volume(25)
        
        #print(self.chosenTrackName)
        
        
        
    def play_chosen_track(self,length,from_time=0):
        self.player.set_time(from_time * 1000)
        self.player.play()
        time.sleep(length)
        self.player.pause()

        
    def search_track(self,string):
        
        optionalTracks = []
        for name in self.playlistTrackName:
            if string.lower() in name.lower():
                optionalTracks.append(name)
                
        return optionalTracks
    
    
    def get_playlist_name(self,playlistID):
        try:
            playlist = self.spotify.playlist(playlistID)
            return playlist['name']
        except:
            return None
        

        

if __name__ == "__main__":
    H = heardle()
    H.add_playlist('2IFfp5anBeKgC2pQySId68')
    H.pick_track()