import serial
import time
import json
    
class arduino():
    
    def __init__(self, com = 'COM5'):
        self.serial = serial.Serial(port = com, baudrate = 9600)
        self.serial_open_time = time.time()
        
        
    def send(self,data):
        if(time.time() > self.serial_open_time + 1): #Check if 1 second has passed since serial object was opened
            self.serial.write(data)
        else:
            time.sleep(1-(time.time() - self.serial_open_time))
            self.send(data)
            
            # time.sleep(1)
            # x = (self.serial.read(1))
            
            
            
    def close(self):
        if(self.serial.is_open): #check if serial object is already closed 
            self.serial.close()
            
    def open(self):
        if(not self.serial.is_open): #check if serial object is already open
            self.serial.open()
            self.serial_open_time = time.time() #save the time the serial object was opened
            
    def read(self):
        return self.serial.read(1)

state_dict = {"on" : 1, "off" : 0}
mode_dict = {"Auto" : 0, "Cool":1,"Dry":2,"Fan":3,"Heat":4}
fan_dict = {"Auto" : 0, "1" : 1, "2" : 2, "3" :3}

def key2val(_dict, key):
    if key in _dict:
        return _dict[key]
    else:
        raise Exception('Unsupported key')
        
        

def json2prot(json_obj):
    
    #Converts the json dictonary to the data that will be sent to the arduino
    
    #Arudino AC Data: 
        #Byte 1 - state on/off (will add auto feedback loop state in the future)
        #Byte 2 - AC Mode
        #Byte 3 - Fan mode
        #Byte 4 - Temprature 
    json_obj = json.loads(json_obj)
    state = key2val(state_dict, json_obj["State"])
    mode = key2val(mode_dict, json_obj["Mode"])
    fan = key2val(fan_dict,json_obj["Fan Speed"])
    temp = json_obj["Temperature"]
    
    byte_data = bytes([state, mode,fan,temp])
    return byte_data
    




if __name__ == "__main__":
    
    ino = arduino()
    
    fid = open("AC.json","r")
    json_data = fid.read()
    fid.close()
    print(json_data)
    
    ino.send(json2prot(json_data))
    
    time.sleep(1)
    ino.close()
    
    