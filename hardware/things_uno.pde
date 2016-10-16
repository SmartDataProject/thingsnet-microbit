#include <SoftwareSerial.h>
#include <TheThingsNetwork.h>

// Before your start, make sure that in the Tools menu, your Board and your
// Port is set to Arduino Leonardo

// After you registered your ABP device, go to The Things Network Dashboard
// and copy the Device Addr, Network Session Key and App Session Key

// Set your Device Address, for example: { 0x02, 0xDE, 0xAE, 0x00 };
const byte devAddr[4] = {  0x49, 0xE1, 0xB7, 0x84  };

// Set your Network Session Key, for example: { 0x2B, 0x7E, 0x15, 0x16, ... };
// This is used by the network to identify your device
const byte nwkSKey[16] =  {0x7B, 0x6F, 0x04, 0x6F, 0x34, 0xD3, 0x40, 0x09, 0xB3, 0x73, 0x34, 0x58, 0x3C, 0xBE, 0x44, 0x7B };

// Set your Application Session Key, for example: { 0x2B, 0x7E, 0x15, 0x16, ... };
// This is used by the network for encryption
const byte appSKey[16] = { 0x00, 0x76, 0xBA, 0x38, 0x6B, 0xA5, 0x79, 0x10, 0x39, 0xAD, 0x41, 0xAC, 0xC9, 0xE8, 0xE3, 0xB9 };

#define debugSerial Serial
#define loraSerial Serial1

#define debugPrintLn(...) { if (debugSerial) debugSerial.println(__VA_ARGS__); }
#define debugPrint(...) { if (debugSerial) debugSerial.print(__VA_ARGS__); }

TheThingsNetwork ttn;
SoftwareSerial mySerial(8, 7);

void setup() {
  // Set up the serial interfaces for the debugging serial monitor and LoRa module
  debugSerial.begin(115200);
  loraSerial.begin(57600);
  
  delay(1000);

  // Initialize and reset The Things Uno
  ttn.init(loraSerial, debugSerial);
  ttn.reset();

  // Here we activate the device with your address and keys
  ttn.personalize(devAddr, nwkSKey, appSKey);

  // Show the status on the debugging serial monitor
  ttn.showStatus();
  debugPrintLn("Setup for The Things Network complete");
  
  mySerial.begin(9600);
  mySerial.listen();
}

void loop() {
  debugPrintLn("Waiting...");
  if (mySerial.available()) {
    ttn.sendBytes(bytearray(readacc()), 6);
  }
  
  // Wait 10 seconds
  delay(1000);
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

int* readacc() {
  String input = "";
  int* output = new int[3];
  char c;
  char nl = '\n';
  while (c != nl) {
    c = mySerial.read();
    input += c;
  }
  debugPrintLn(input);
  output[0] = getValue(input, ',', 0).toInt();
  output[1] = getValue(input, ',', 1).toInt();
  output[2] = getValue(input, ',', 2).toInt();
  return output;  
}

byte* bytearray(int* input) {
  byte* output = new byte[6];
  int index = 0;
  for (int i=0; i<3; i++) {
    index = 2 * i;
    output[index] = lowByte(input[i]);
    output[index+1] = highByte(input[i]);
  }
  return output;
}