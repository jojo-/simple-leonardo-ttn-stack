# Connecting a Leonardo to the LoraWan
#
# This sketch reads values from load cells and then
# sends them over the LoraWan network.
#
# Author: J. Barthelemy
#
# Version: 18 Apr 2017

#include <Q2HX711.h>

// Constants and global variables

// ... scale
const byte hx711_clock_pin = A1;
const byte hx711_data_pin = A2;
const int samples = 3;
const long calibration = 8059052;
Q2HX711 hx711(hx711_data_pin, hx711_clock_pin);

// ... lorawan
const char ATappEui[] = "AT+NI=0,<appEui>";
const char ATappKey[] = "AT+NK=0,<appKey>";

void setup() {

  // init the serial interfaces
  Serial.begin(115200);  // RX/TX via USB
  Serial1.begin(115200); // RX/TX on the board

  // joigning lorawan
  join_lora();
  
}

// reading samples values from the sensor and average it
int read_weight() {
  
  long average = 0;
  for(int i = 0; i < samples; i++) {
    average = average + hx711.read();
  }
  average = average / (long)samples;
  
  return (average - calibration) / 10000;

}

// sending data over lorawan
void send_data(int val, char* msg1, char* msg2) {

  // prepare the payload
  char at_payload[20];
  memset(at_payload,'\0', 20);
  const char sep[] = ";";
  strcat(at_payload,"AT+SEND=");

  // ... adding the latitude
  strcat(at_payload, msg1);
  strcat(at_payload, sep);

  // ... adding the longitude
  strcat(at_payload, msg2);
  strcat(at_payload, sep);

  // ... adding the weight
  char val_str[3];
  sprintf(val_str, "%d", val);
  strcat(at_payload, val_str);

  Serial.println(at_payload);

  // send it via lorawan
  send_at_command(at_payload,"OK",10000);

}

// sending AT commands to the LoraWan module
void send_at_command(const char* cmd, const char* expected_ans, int waiting_period) {

  // cleaning buffer
  while (Serial1.available() > 0) Serial1.read();

  char response[200];
  memset(response, '\0', 200);

  bool ack = false;
  while (ack == false) {
 
    // sending the command and waiting
    Serial1.println(cmd);
    delay(waiting_period);
    
    // receiving the answer 
    uint8_t i = 0;
    while (Serial1.available() > 0) {
      response[i] = Serial1.read();
      i++;      
    }
    Serial.write(response);

    // check received answer with expectation
    if (strstr(response, expected_ans) != NULL) {
      ack = true;
    }

  }

}

// joining the lorawan network
void join_lora() {

  send_at_command("AT","OK",500);
  send_at_command("AT","OK",500);
  send_at_command("AT+PN=1","OK",500);
  send_at_command("AT+FSB=2","OK",500);
  send_at_command("AT+NJM=1","OK",500);
  send_at_command(ATappEui,"ID",1000);
  send_at_command(ATappKey,"Key",1000);
  send_at_command("AT+TXP=20","OK",500);
  send_at_command("AT+JOIN","OK",10000);

}

void loop() {

  // get weight
  int w = read_weight();
 
  // get location (UOW)
  char loc_a[] = "uow";
  char loc_b[] = "bl6";

  // send data
  send_data(w, loc_a, loc_b);
  
  // stop for 1 minute (later on: can be put to sleep)
  delay(60000);

}
