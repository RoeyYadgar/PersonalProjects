# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 19:11:50 2021

@author: User
"""

import serial_comm
import socket
import json
import threading
import os
import socket_comm
from datetime import datetime
import time

port = 5050
server = socket.gethostbyname(socket.gethostname())
addr = (server,port)
header = 2

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(addr)

server_running = True

def handle_arduino():
    global ino
    ino = serial_comm.arduino()
    print("arudino connected")
    while (ino.serial.is_open and server_running):
        data = str(int.from_bytes(ino.read(),"big"))
        log_data("temperature.txt", data)      
    
def handle_client(conn,addr):
    connected= True
    fid = open('AC.json','r')
    json_data = fid.read()
    fid.close()
    
    socket_comm.send(conn,json_data)
    
    while connected:
        
        msg = socket_comm.read(conn)
        print(msg)
        if msg == "close":
            print("connection closed")
            connected = False
        elif msg == "quit":
            connected = False
            stop_server()
        else:
            ino.send(serial_comm.json2prot(msg))
            write_json_state(msg)
            log_data("commands.txt",msg)
            
    conn.close()
        
        

def start_server():
    global ino_thread
    server.listen()
    ino_thread = threading.Thread(target = handle_arduino,args = ())
    ino_thread.start()
    while True:
        conn, conn_addr = server.accept()
        print("client connected")
        thread = threading.Thread(target = handle_client, args=(conn,conn_addr))
        thread.start()
    
def stop_server():
    global server_running
    print("server sutting down")
    server_running = False
    while ino_thread.is_alive():
        time.sleep(0.1)
    ino.close()
    os._exit(1)    

def write_json_state(data):
    fid = open('AC.json','w')
    fid.write(data)
    fid.close()
    
def log_data(path,data):
    fid = open(path,'a')
    fid.write(datetime.now().strftime("%D %H:%M:%S") + " - " +data + "\n")
    fid.close()
    
    
start_server()