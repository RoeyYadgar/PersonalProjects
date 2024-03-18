#include <Tadiran.h>
#include <IRremote.h>
#include <dht11.h>
IRsend irsend(21);

Tadiran tadiran(0,0,24,false);
int state,mode,fan,temp;
bool data_valid;

dht11 DHT11;
int counter = 0;
#define dhtpin 2

bool validate_data(){
  //Check that each field has a valid value
  if(0 > state || state > 1){
    return false;
  }

  if(0 > mode || mode > 4)
  {
    return false;
  }

  if(0 > fan || fan > 3)
  {
    return false;
  }

  if(16 > temp || temp > 26)
  {
    return false;
  }

  return true;
}

void modify_tadiran()
{
  //Modify the tadiran object with the new values
  tadiran.setState(state);
  tadiran.setMode(mode);
  tadiran.setFan(fan);
  tadiran.setTemeprature(temp);
  
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  while(Serial.available() > 0)
  {
    //Message will always be 4 bytes long read the 4 bytes
    state = Serial.read();
    mode = Serial.read();
    fan = Serial.read();
    temp = Serial.read();
    
    data_valid = validate_data(); //check for valid values

   
    
    if(data_valid) //if data is valid modify tadiran object, send the IR signal, and send over serial indication for valid data
    {
      modify_tadiran();
      irsend.sendRaw(tadiran.codes,TADIRAN_BUFFER_SIZE,38);
      //Serial.write((byte) 0x00); 
    }
    else{ //if data is not valid send back FF to indicate for invalid data
      //Serial.write((byte) 0xFF);
    }
  }
  counter++;
  if(counter == 59)
  {
    counter = 0;
    int chk = DHT11.read(dhtpin);
    Serial.write((byte) DHT11.temperature);
  }
  delay(1000);
}
