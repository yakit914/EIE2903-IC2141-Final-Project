from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time
import threading
import Adafruit_DHT
import Adafruit_ADS1x15
import paho.mqtt.client as mqtt
import signal
import json
import math
import random
import sys

GPIO.setwarnings(False)

flag = False
flag1 = False
CURRENT_STATE = "Available"

NODE_ID = "B08"
loc = "W311D-Z2"

#mqtt_topic = "iot/24074014d"
mqtt_topic = "iot/sensor-B08"
Mode_Switch_topic = "IC/TM1118/TEAM_B08/PUB"


GAIN = 1
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
Light_PIN = 25
adc = Adafruit_ADS1x15.ADS1115()
lcd = CharLCD('PCF8574',0x27,charmap='A00')
output_channel = [8]

client1 = mqtt.Client("iot-24074014d") # Create a Client Instance
client2 = mqtt.Client("iot-24132859d") 
#mqtt_broker = "broker.hivemq.com" # Broker
mqtt_broker = "ia.ic.polyu.edu.hk" # Broker
mqtt_port = 1883 # Default
mqtt_qos = 1 # Quality of Service = 1
client1.connect(mqtt_broker, mqtt_port) # Establish a connection to a broker
client2.connect(mqtt_broker, mqtt_port)

client1.subscribe(mqtt_topic, mqtt_qos)
client2.subscribe(Mode_Switch_topic , mqtt_qos)

Timer_reset = 5
atimer = 5

Light_Min = 1493
Light_Max = 25294

flag = False
flag2 = False
warn = False

##
ground = [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1]
Player_position = 0
Player_state = 'Run'
Score = 0
Game_state = "Start"

BUTTON_GPIO = 20
SW1_BUTTON = 21

lcd = CharLCD('PCF8574',0x27,charmap='A00')

Run1 = (
    0b01110,
    0b01110,
    0b10100,
    0b11111,
    0b00101,
    0b00110,
    0b11001,
    0b00001,
)

Run2 = (
    0b01110,
    0b01110,
    0b00101,
    0b11111,
    0b10100,
    0b00110,
    0b11001,
    0b00001,
)

Jump = (
    0b01110,
    0b01110,
    0b10101,
    0b11111,
    0b00100,
    0b01111,
    0b01001,
    0b00000,
)

Fall= (
    0b01110,
    0b01110,
    0b10101,
    0b11111,
    0b00100,
    0b00111,
    0b00100,
    0b00111,
)

Earth= (
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
)

lcd.create_char(0,Run1)
lcd.create_char(1,Run2)
lcd.create_char(2,Jump)
lcd.create_char(3,Fall)
lcd.create_char(4,Earth)
##

def random_hole():
    random.seed(time.time())
    output = []
    hole_no = random.randint(1,3)
    if hole_no == 1:
        output.append(random.randint(3, 13))
    elif hole_no == 2:
        output.append(random.randint(3, 6))
        output.append(random.randint(8, 13))
    elif hole_no == 3:
        output.append(random.randint(3, 5))
        output.append(random.randint(7, 10))
        output.append(random.randint(12, 14))
    return output

def update_hole():
    global ground
    hole = random_hole()
    for i in range(0,len(ground)):
        if i in hole:
            ground[i] = 0
        else:
            ground[i] = 1

def check_ground_collapse():
    global Player_state
    global Player_position
    global ground
    global Score
    if ground[Player_position] == 0:
        if Player_state != 'Jump':
            Player_state = 'FALLING'
            for i in ground :
                if i == 0:
                    ground[Player_position] = 3
        else:
            Score += 1

Flag = False
def display():
    
    global Player_state
    global Player_position
    global ground
    global Flag
    global Score
    Flag = not Flag
    
    for i in range(0,16-1):
        if Player_position == i and Player_state =='Run':
            lcd.cursor_pos = (0,i)
            if Flag:
                lcd.write_string('\x00')
            else:
                lcd.write_string('\x01')
        elif Player_position == i and Player_state == 'FALLING':
            lcd.cursor_pos=(0,i)
            lcd.write_string(' ')
        elif Player_position == i and Player_state == 'Jump':
            lcd.cursor_pos = (0,i)
            lcd.write_string('\x02')
        else:
            lcd.cursor_pos = (0,i)
            lcd.write_string(' ')
            
    
        
    for i in range(0,len(ground)):
        if ground[i] == 1 :
            lcd.cursor_pos = (1,i)
            lcd.write_string('\x04')
        elif ground[i] == 3:
            lcd.cursor_pos = (1,i)
            lcd.write_string('\x03')
        else:
            lcd.cursor_pos = (1,i)
            lcd.write_string(' ')
    
    lcd.cursor_pos = (0,15)
    lcd.write_string(str(Score))
    
    if Player_state == 'FALLING':
        lcd.cursor_pos=(0,0)
        lcd.write_string('Game Over!')

def Playing():
    move_player()
    display()
    
def Start_m():
    lcd.cursor_pos = (0,0)
    lcd.write_string(f'{"SW2:start/jump":<16}')
    lcd.cursor_pos = (1,0)
    lcd.write_string(f'{"SW1:reset":<16}')


def signal_handler(sign, frame):
    GPIO.cleanup
    sys.exit

def move_player():
    global Player_state
    global Player_position
    global ground
    if Player_state == 'Run' or Player_state == 'Jump':
        if Player_position >=0 and Player_position <15:
            Player_position += 1
        else:
            update_hole()
            Player_position = 0
    check_ground_collapse()
    print("Position: ", Player_state, "Position: ", Player_position)

def jump_to_run():
    global Player_state
    global Player_position
    global ground
    
    Player_state = 'Run'

def Jump():
    global Game_state
    global Game_state
    global Player_state
    global Player_position
    global ground
    if Player_state == 'Run':
        Player_state = 'Jump'
        timer = threading.Timer(1,jump_to_run)
        timer.start()

def Reset():
    global Game_state
    global Player_state
    global Player_position
    global ground
    global Score
    if Player_state == 'FALLING':
        lcd.clear()
        for i in ground :
            if i == 3:
                ground[Player_position] = 0
        Player_position = 0
        Player_state = 'Run'
        Score = 0
        Game_state = 'Start'
        lcd.clear()
        
def Force_game_reset():
    global Game_state
    global Game_state
    global Player_state
    global Player_position
    global ground
    lcd.clear()
    for i in ground :
        if i == 3:
            ground[Player_position] = 0
    Player_position = 0
    Player_state = 'Run'
    Score = 0
    Game_state = 'Start'
    lcd.clear()

def Ave_reset():
    global atimer,Timer_reset,warn
    warn = False
    atimer = Timer_reset
    lcd.clear()
    p.stop()
    lcd.cursor_pos = (0,0)
    lcd.write_string(f'{"TEAM B08 Node":^16}')
    lcd.cursor_pos = (1,0)
    lcd.write_string(f'{"Mode Swap!":^16}')
    
def Reset_everything():
    Force_game_reset()
    Ave_reset()
    
    
def Start_game():
    global Game_state
    Player_position = 0
    Player_state = 'Run'
    Score = 0
    Game_state = 'Play'



def mode_on_message(client, userdata, msg):
    global CURRENT_STATE
    try:
        d_msg = str(msg.payload.decode("utf-8"))
        iotData = json.loads(d_msg)
        print("Received message on topic %s : %s" % (Mode_Switch_topic, iotData))
        if CURRENT_STATE != iotData["Status"]:
            Reset_everything()
            CURRENT_STATE = iotData["Status"]
        
        print("updated state: ", CURRENT_STATE)
        if CURRENT_STATE == "Stop":
            lcd.clear()
            lcd.cursor_pos = (0,0)
            lcd.write_string(f'{"Standby":^16}')
            lcd.cursor_pos = (1,0)
            lcd.write_string(f'{"Mode":^16}')
            GPIO.output(output_channel ,GPIO.LOW)
    except Exception as e:
            print("error: ",e)


def mqtt_on_message(client, userdata, msg):
    global atimer,Timer_reset, CURRENT_STATE
    if (CURRENT_STATE == "Available"):
        try:
            AlertDic = {"hot": "Too Hot","cold": "Too cold","light": "Too Bright", "snd": "Too loud"}
            d_msg = str(msg.payload.decode("utf-8"))
            iotData2 = json.loads(d_msg)
            #print("Received message on topic %s : %s" % (msg.topic, iotData2))
            
            #p = Event(node_id=iotData["node_id"], loc=iotData["loc"], temp=iotData["temp"],hum=iotData["hum"],light = iotData["light"], snd =iotData["snd"])
            if float(iotData2['temp']) >= 30:
                lcd.clear()
                lcd.cursor_pos = (0,0)
                lcd.write_string(AlertDic["hot"])
                atimer = 0
            elif float(iotData2['temp']) <= 10:
                lcd.clear()
                lcd.cursor_pos = (0,0)
                lcd.write_string(AlertDic["cold"])
                atimer = 0
            elif float(iotData2['light']) >= 50: #30
                lcd.clear()
                lcd.cursor_pos = (0,0)
                lcd.write_string(AlertDic["light"])
                atimer = 0
            elif float(iotData2['snd']) >= 100: #65
                lcd.clear()
                lcd.cursor_pos = (0,0)
                lcd.write_string(AlertDic["snd"])
                atimer = 0
        except Exception as e:
                pass
    

buzzer_flag = False
def buzzer_control():
    global buzzer_flag
    timer = threading.Timer(1,buzzer_control) #after 3s, call timer()
    timer.start() #creating a timer object named as timer with start function
    buzzer_flag = not buzzer_flag
    if buzzer_flag:
        for dc in range(0, 1,25):
                p.ChangeDutyCycle(dc)
    else:
        for dc in range(1,-1,-25):
                p.ChangeDutyCycle(dc) 




def timer_interrupt():
    global flag ,Timer_reset,atimer,CURRENT_STATE# global timer
    timer = threading.Timer(1,timer_interrupt) #after 3s, call timer()
    timer.start() #creating a timer object named as timer with start function
    flag = not(flag)
    if CURRENT_STATE == "Available":
        if flag == True:
            GPIO.output(output_channel ,GPIO.HIGH)
        else:
            GPIO.output(output_channel ,GPIO.LOW)
        if atimer < Timer_reset:
            warn = True
            p.start(0)
            atimer +=1
        elif atimer >= Timer_reset:
            warn = False
            p.stop()
    

    
def SW2_callback(channel):
    global Game_state
    global Player_state
    global Player_position
    global ground,CURRENT_STATE
    if (CURRENT_STATE == "Game"):
        if Game_state == 'Start':
            Start_game()
        elif Game_state == 'Play':
            Jump()

def SW1_callback(channel):
    global Game_state
    global Player_state
    global Player_position
    global ground
    global Score,CURRENT_STATE
    if (CURRENT_STATE == "Game"):
        if Game_state == 'Play':
            Reset()


GPIO.setmode(GPIO.BCM)
GPIO.setup(output_channel, GPIO.OUT,initial=GPIO.LOW)
GPIO.output(output_channel ,GPIO.LOW)
GPIO.setup(26,GPIO.OUT)

p = GPIO.PWM(26,10)

client1.on_message = mqtt_on_message
client2.on_message = mode_on_message
buzzer_control()
client1.loop_start()
client2.loop_start()
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(SW1_BUTTON, GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING,
                        callback = SW2_callback, bouncetime=200)

GPIO.add_event_detect(SW1_BUTTON, GPIO.RISING,
                        callback = SW1_callback, bouncetime=200)

def signal_handler(sign, frame):
    GPIO.cleanup
    sys.exit
    
signal.signal(signal.SIGINT,signal_handler)
warn = False
timer_interrupt()
p.stop()
Reset_everything()
while True:
    if (CURRENT_STATE == "Available"):
            try:
                print("program started")
                if not warn:
                    lcd.clear()
                    lcd.cursor_pos = (0,0)
                    lcd.write_string(f'{"TEAM B08 Node":^16}')
                    lcd.cursor_pos = (1,0)
                    lcd.write_string(f'{"Now Operating!":^16}')
                Light_ADC = adc.read_adc(3, gain= GAIN)
                Sound_ADC = adc.read_adc(2, gain= GAIN)+600
                if (Sound_ADC/1300) <= 0.1:
                    Sound_LV = -99*20 + 80
                else:
                    Sound_LV = 20*(math.log(Sound_ADC/1300)) + 80
                voltage = (Light_ADC/2**15)*4.096/GAIN
                #Light_LV = ((2500/Votage_value)-500)/3.3
                #v_ldr = 3.3 * (voltage / (voltage + 10000)) 
                #Light_LV = (3.3 - v_ldr) / (v_ldr / 10000)
                Light_LV = ( Light_ADC / (Light_Max))*100
                if Light_LV >= 100:
                    Light_LV = 100
                elif Light_LV <= 0:
                    Light_LV = 0
                
                #print("sound: ",Sound_LV)
                humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
                
                Light = str(int(round(Light_LV)))
                Sound = str(int(round(Sound_LV)))
                humidity = str(humidity)
                temperature = str(temperature)
                
                iotDic = {"node_id":NODE_ID ,"loc":loc,"temp":temperature,"hum":humidity,"light":Light,"snd":Sound}
                jsonData = json.dumps(iotDic) # Encode iotDic object to JSON
                #print(jsonData)

                client1.publish(mqtt_topic, jsonData, mqtt_qos) # Publish a message

                print("Publishing message", jsonData ,"to topic", mqtt_topic)
                for i in range(10):
                    if CURRENT_STATE == "Available":
                        time.sleep(1)
                
                
                
            except KeyboardInterrupt:
                lcd.clear()
                lcd.cursor_pos = (1,3)
                time.sleep(1)
                lcd.backlight_enabled=False
                GPIO.cleanup()
                lcd.backlight_enabled=False
    elif (CURRENT_STATE == "Game"):
        if Game_state == 'Start':
            Start_m()
        elif Game_state == 'Play':
            Playing()
        time.sleep(1)

        






