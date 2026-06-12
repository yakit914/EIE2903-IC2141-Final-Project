#include <WiFi.h>               // Wifi driver
#include <PubSubClient.h>       // MQTT server library
#include <ArduinoJson.h>        // JSON library
//#include <M5StickC.h>
#include <M5StickCPlus2.h>
#include <DFRobot_DHT11.h>      // DHT11 library
//#include <Arduino.h>


#define DATA 0                  // DHT11 data pin
#define ID 9
#define LED 26

// DHT11
DFRobot_DHT11 dht;

// Operating parameters
float temp,hum;
bool Flag = false;
bool warning = false;

// MQTT and WiFi set-up
WiFiClient espClient;
PubSubClient client(espClient);
//Neotimer mytimer(900000); // Set timer interrupt to 15min

// Key debounce set-up
//ButtonDebounce trigger(TRIG, 100);//IO debouncing
//ButtonDebounce function_key(FUNC_KEY, 100); //IO debouncing

//const char *ssid = "TM0512";              // Your SSID             
//const char *password = "05120512";             // Your Wifi password
const char *ssid = "icw502g";              // Your SSID             
const char *password = "8c122ase";             // Your Wifi password
//const char *ssid = "EIA-W311MESH";              // Your SSID             
//const char *password = "42004200";             // Your Wifi password
//const char *mqtt_server = "broker.hivemq.com"; // MQTT server name
const char *mqtt_server = "ia.ic.polyu.edu.hk"; // MQTT server name
//const char *mqtt_server = "192.168.0.170";
//char *mqttTopic = "IC/TeamB08";
char *mqttTopic = "iot/sensor-B08";

byte reconnect_count = 0;
long currentTime = 0;

char msg[100];
String ipAddress;
String macAddr;

StaticJsonDocument<100> Jsondata; // Create a JSON document of 200 characters max

//Set up the Wifi connection
void setup_wifi() {
  byte count = 0;
  
  WiFi.disconnect();
  delay(100);
  // We start by connecting to a WiFi network
  Serial.printf("\nConnecting to %s\n", ssid);
  WiFi.begin(ssid, password); // start the Wifi connection with defined SSID and PW

  // Indicate "......" during connecting
  // Restart if WiFi cannot be connected for 30sec
  currentTime = millis();
  M5.Lcd.setCursor(0,0);
  M5.Lcd.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    M5.Lcd.print(".");
    count++;
    if (count == 6) {
      count = 0;
      M5.Lcd.setCursor(0,0);
      M5.Lcd.print("Connecting       "); //clear the dots
      M5.Lcd.setCursor(0,0);
    }
      
    if (millis()-currentTime > 30000){
      ESP.restart();
    }
  }
  // Show "WiFi connected" once linked and light up LED1
  Serial.printf("\nWiFi connected\n");
  // Show IP address and MAC address
  ipAddress=WiFi.localIP().toString();
  Serial.printf("\nIP address: %s\n", ipAddress.c_str());
  macAddr=WiFi.macAddress();
  Serial.printf("MAC address: %s\n", macAddr.c_str());
  
  //Show in the small TFT
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setCursor(0,0);
  M5.Lcd.print("WiFi connected!");
  delay(3000);
  M5.Lcd.fillScreen(BLACK);
}

/*// Routine to receive message from MQTT server
void callback(char* topic, byte* payload, unsigned int length) {
  
  recMsg ="";
  for (int i = 0; i < length; i++) {
    recMsg = recMsg + (char)payload[i];
  }
  Serial.printf("%d: Message arrived [%s] %s\n", millis(), topic, recMsg.c_str());
  Serial.println(recMsg);
  delay(500);
}*/

/*//void callback(char* topic, byte* payload, unsigned int length) {
  
  char recMsg[] ="";
  for (int i = 0; i < length; i++) {
    recMsg = recMsg + (char)payload[i];
  }
  Serial.printf("%d: Message arrived [%s] %s\n", millis(), topic, recMsg.c_str());
  Serial.println(recMsg);
  delay(500);
}*/


// Reconnect mechanism for MQTT Server
void reconnect() {
  // Loop until we're reconnected
  
  while (!client.connected()) {
    Serial.printf("Attempting MQTT connection...");
    // Attempt to connect
    //if (client.connect("ESP32Client")) {
    if (client.connect(macAddr.c_str())) {
      Serial.println("Connected");
      // Once connected, publish an announcement...
      snprintf(msg, 75, "IoT System (%s) is READY", ipAddress.c_str());
      client.subscribe(mqttTopic);
      delay(1000);
      client.publish(mqttTopic, msg);
      reconnect_count = 0;
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      reconnect_count++;
      
      //reconnect wifi by restart if retrial up to 5 times
      if (reconnect_count == 5){
        ESP.restart();//reset if not connected to server 
      }
        
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  auto cfg = M5.config();
  StickCP2.begin(cfg);

  Serial.begin(115200); 
  Serial.println("System Start!");  
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  
  M5.begin();
  
  M5.Lcd.setRotation(3);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextSize(2);

  M5.Speaker.setVolume(200);
  
  setup_wifi();
  
  client.setServer(mqtt_server, 1883);
  //client.setCallback(callback);

  const char* NODE_ID = "B08-M06";
  const char* loc = "W311D-Z2";
  int light;
  float snd;

  //Initalize Json message
  Jsondata["node_id"] = NODE_ID;
  Jsondata["loc"] = loc; 
  Jsondata["temp"] = temp;
  Jsondata["hum"] = hum;
  Jsondata["light"] = light;
  Jsondata["snd"] = snd; 

  M5.Lcd.setCursor(0, 0);
  M5.Lcd.println("TEMP/C  HUM/%");
}

void Alert_on_off()
{
  if (StickCP2.BtnA.wasPressed() || StickCP2.BtnB.wasPressed() ) 
      {
        warning = !(warning);
        M5.Lcd.setTextColor(RED);
        M5.Lcd.setCursor(20, 60);
        if (warning)
        {
          M5.Lcd.print("Alert On!");
        }
        else
        {
          M5.Lcd.print("Alert Off!");
        }
        delay(1000);
        M5.Lcd.setTextColor(WHITE);
        M5.Lcd.fillRect(20, 40, 500, 40, BLACK);
      }
}

void loop() {
  StickCP2.update();
  Alert_on_off();

  if (!client.connected()){
    reconnect();
   }
  client.loop();

  // DHT11
  // Measure temp & hum from DHT11
  // Measure temp & hum
  dht.read(DATA);
  hum = dht.humidity;  
  temp = dht.temperature; // in Celcius 
  
  M5.Lcd.fillRect(20, 20, 500, 40, BLACK);
  M5.Lcd.setCursor(20, 20);
  M5.Lcd.printf("%4.1f  %4.1f", temp, hum);

  if (warning)
  {
    if (temp >= 30)
    { 
      Flag = true;
      M5.Lcd.setTextColor(RED);
      M5.Lcd.setCursor(20, 40);
      M5.Lcd.print("Too Hot!");
    }
  else if (temp <= 10)
    { 
      Flag = true;
      M5.Lcd.setTextColor(BLUE);
      M5.Lcd.setCursor(20, 40);
      M5.Lcd.print("Too Cold!");
    }
  if (hum >= 70)
    { 
      Flag = true;
      M5.Lcd.setTextColor(BLUE);
      M5.Lcd.setCursor(20, 40);
      M5.Lcd.print("Too Wet!");
    }
  }

  if (Flag && warning)
  {
    M5.Lcd.setCursor(20, 60);
    M5.Lcd.setTextColor(RED);
    M5.Lcd.print("WARNING!!!");
    StickCP2.Speaker.tone(100000, 5000);
    delay(1000);
  }

  M5.Lcd.fillRect(20, 40, 500, 40, BLACK);
  M5.Lcd.setTextColor(WHITE);
  M5.Speaker.stop();

  Jsondata["temp"] = temp;
  Jsondata["hum"] = hum;

  char buffer[256];
  serializeJson(Jsondata, buffer);
  client.publish(mqttTopic, buffer);
  //client.publish(mqttTopic, msg);

  // For Humidity  
  Serial.print("Humidity : ");  
  Serial.print(hum);
  Serial.println("%");  
  // For Temprature   
  Serial.print("Temperature : ");  
  Serial.print(temp);  
  Serial.println("degC ");  

  digitalWrite(LED,digitalRead(LED)^1);
  delay(2000);
}
