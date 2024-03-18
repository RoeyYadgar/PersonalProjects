
import threading
import stdioImpl
import sys
import socket
import socket_comm
import json
import time
from datetime import datetime
from logipy import logi_led

port = 5051
server = socket.gethostbyname(socket.gethostname())
addr = (server,port)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(addr)
server.listen()
serverRunning = True

RGBnumpadcodes = [0x45,0x135,0x37,0x4a,0x47,0x48,0x49,0x4e,0x4b,0x4c,0x4d,0x4f,0x50,0x51,0x11c,0x52
               ,0x53]
               
ModeRGB = {"Off" : (0,100,0), 
    "Youtube" : (100,0,0),
    "Twitch" : (50,0,100),
    "Mako" : (0,0,100),
    "Netflix" : (100,100,100),
    "Kan" : (0,0,0)}
#currentMode = "Off"

def dbgTest(msg):
    fid = open('test.txt','a')    
    fid.write(datetime.now().strftime("%D %H:%M:%S") + " - " + msg)
    fid.close()
    return


def nativeMessageInput():
    while True:
        message = stdioImpl.get_message()
        if(message == None):
            dbgTest("Exiting Program \n")
            closeServer()
            return
        else:
            dbgTest("Native Message Log : " + str(message)+"\n")
            
            


def handle_client(conn,addr):
    connected = True
    while connected:
        msg = socket_comm.read(conn)
        if msg == "close":
            #dbgTest("connection closed \n")
            connected = False
        else:
            #dbgTest("Message Received : " +str(msg) + "\n")
            handle_client_msg(msg)
            
    conn.close()
    

def handle_client_msg(msg):
    jsonContent = json.loads(msg)
    
    if("Mode" in jsonContent):
        rgbcode = ModeRGB[jsonContent["Mode"]]
        for code in RGBnumpadcodes:
            logi_led.logi_led_set_lighting_for_key_with_key_name(code, rgbcode[0], rgbcode[1], rgbcode[2])
            

    stdioImpl.send_message(jsonContent)
    return 
    

def socketServer():
    while serverRunning:
        conn, conn_addr = server.accept()
        #dbgTest("Client Connected \n")
        thread = threading.Thread(target = handle_client, args = (conn,conn_addr))
        thread.daemon = True
        thread.start()

def backgroundRun(): #Used to keep the chrome service worker running by sending a message every once in a while
    while serverRunning:
        time.sleep(60)
        stdioImpl.send_message("pong")

def Main():
    global nativeThread 
    global socketThread

    logi_led.logi_led_init() #Keyboard led lighting setup


    nativeThread = threading.Thread(target = nativeMessageInput,args = ())
    nativeThread.start()

    socketThread = threading.Thread(target = socketServer,args = ())
    socketThread.daemon = True
    socketThread.start()

    backgroundRunThread = threading.Thread(target = backgroundRun,args = ())
    backgroundRunThread.daemon = True
    backgroundRunThread.start()


def closeServer():
    global serverRunning
    serverRunning = False
    
    logi_led.logi_led_shutdown()

    sys.exit(0)


Main()