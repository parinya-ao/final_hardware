from machine import Pin, ADC ,I2C, Timer, PWM
from hashlib import sha256
import time
import ssd1306
import network
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS,
    TOPIC_PREFIX
)
from umqtt.simple import MQTTClient
from servo import Servo
speak_val = False

servo = Servo(12)
Unlock_door = False
RED_GPIO = 42
YELLOW_GPIO = 41
GREEN_GPIO = 40
SWITCH1_GPIO = 2
SWITCH2_GPIO = 1
SPEAKER_PIN = 13
TOPIC_LIGHT = f'{TOPIC_PREFIX}/light'
TOPIC_LED_RED = f'{TOPIC_PREFIX}/led/red'
TOPIC_LED_YELLOW = f'{TOPIC_PREFIX}/led/yellow'
TOPIC_LED_GREEN = f'{TOPIC_PREFIX}/led/green'
TOPIC_LED_SWITCH = f'{TOPIC_PREFIX}/switch'
TOPIC_LED_TEXT = f'{TOPIC_PREFIX}/text'
TOPIC_UNLOCK = f'{TOPIC_PREFIX}/nfclocking'
OFSD_ONOFF = f'{TOPIC_PREFIX}/OFSD'
TOPIC_OFFICE = f'{TOPIC_PREFIX}/office'


def get_key():
    key = 0
    for col_num, col_pin in enumerate(cols):
        Pin(col_pin).value(1)
        for row_num, row_pin in enumerate(rows):
            if Pin(row_pin).value():
                key = keys[row_num][col_num]
        Pin(col_pin).value(0)
    return key

def connect_wifi():
    mac = ':'.join(f'{b:02X}' for b in wifi.config('mac'))
    print(f'WiFi MAC address is {mac}')
    wifi.active(True)
    print(f'Connecting to WiFi {WIFI_SSID}.')
    wifi.connect(WIFI_SSID, WIFI_PASS)
    while not wifi.isconnected():
        print('.', end='')
        time.sleep(0.5)
    print('\nWiFi connected.')

def connect_mqtt():
    print(f'Connecting to MQTT broker at {MQTT_BROKER}.')
    mqtt.connect()
    mqtt.set_callback(mqtt_callback)
    mqtt.subscribe(TOPIC_LED_RED)
    mqtt.subscribe(TOPIC_LED_YELLOW)
    mqtt.subscribe(TOPIC_LED_GREEN)
    mqtt.subscribe(TOPIC_LED_TEXT)
    mqtt.subscribe(TOPIC_UNLOCK)
    mqtt.subscribe(TOPIC_OFFICE)
    
    
    print('MQTT broker connected.')
    
def mqtt_callback(topic, payload):
    global Unlock_door
    global text
    
    if topic.decode() == TOPIC_LED_RED:
        try:
            red.value(int(payload))
        except ValueError:
            pass
        
    if topic.decode() == TOPIC_UNLOCK:
        try:
            Unlock_door = bool(int(payload))
            if Unlock_door:
                display.fill(0)
                text = "UNLOCK"
                green_LED.value(1)
            else:
                display.fill(0)
                text = "LOCK"
                green_LED.value(0)
                red_LED.value(1)
                #time.sleep(1)
                red_LED.value(0)
        except ValueError:
            pass
    if topic.decode() == TOPIC_OFFICE:
        global speak_val
        print(payload)
        if int(payload) == 1:
            speak_val = True
        if int(payload) == 0:
            speak_val = False

def Timer_callback(T):
    global speaker_oo
    speaker_oo = speak_val

############
# setup
############
red_LED = Pin(RED_GPIO, Pin.OUT)
green_LED = Pin(GREEN_GPIO, Pin.OUT)
sw1 = Pin(SWITCH1_GPIO, Pin.IN, Pin.PULL_UP)
sw2 = Pin(SWITCH2_GPIO, Pin.IN, Pin.PULL_UP)
speaker = PWM(Pin(SPEAKER_PIN))
speaker.duty_u16(0)
rows = [6, 18, 17, 15]
cols = [7, 5, 16]
for row_pin in rows:
    Pin(row_pin, Pin.IN, Pin.PULL_DOWN)
for col_pin in cols:
    Pin(col_pin, Pin.OUT)
keys = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']]
entered_pass = ""
correct_pass = b'\xc9zj\x12@y\xde\xc9I\r\x8f\x1c\xcd*\xe5\r\xa4\xd0g\xe7ID\x10\x02\xdcm\xb4\xfd_\x98y\r'
text = "LOCK"

i2c = I2C(0, sda=Pin(48), scl=Pin(47))
display = ssd1306.SSD1306_I2C(128,64,i2c)
display.text('Enter your', 5, 0, 1)
display.text('password :', 5, 12, 1)
display.show()

wifi = network.WLAN(network.STA_IF)
mqtt = MQTTClient(client_id='',
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
connect_wifi()
connect_mqtt()

speaker_oo = False
start_time = time.time()
current_time = time.time()

max_loop_time = 10

tim = Timer(1)
tim.init(period=15000, callback=Timer_callback)

############
# loop
############
while True:
    display.text('Enter your', 5, 0, 1)
    display.text('password :', 5, 12, 1)
    display.text(text, 5, 36, 3)
    display.show()
    mqtt.check_msg()
    
    if sw1.value() == 0:
        Unlock_door = False
        speaker_oo = False
        green_LED.value(0)
        red_LED.value(1)
        text = "LOCK"
        display.fill(0)
        #time.sleep(1)
        red_LED.value(0)
            
        while True:
            if sw1.value() == 1:
                break
            
    if sw2.value() == 0:
        Unlock_door = True
        text = "UNLOCK"
        display.fill(0)
    
    if Unlock_door == True:
        green_LED.value(1)
        red_LED.value(0)
        servo.write(0)
        key = get_key()
        if key == "*":
            Unlock_door = False

    
    if Unlock_door != True:
        servo.write(180)
        key = get_key()
        if key :
            if key == "#":
                print()
                if sha256(entered_pass.encode()).digest() == correct_pass:
                    text = "UNLOCK"
                    Unlock_door = True
                    green_LED.value(1)
                else:
                    red_LED.value(1)
                    text = "LOCK"
                display.fill(0)
                entered_pass = ""
                #time.sleep(1)
                red_LED.value(0)
            elif key == "*":
                green_LED.value(0)
                red_LED.value(1)
                text = "LOCK"
                display.fill(0)
                entered_pass = ""
                #time.sleep(1)
                red_LED.value(0)
            else:
                print(key, end="")
                entered_pass += key
                display.text(entered_pass, 5, 24, 3)
                display.show()
        while True:
            key = get_key()
            if key == 0:
                break
            time.sleep(0.05)
    
    if speaker_oo == True:
        speaker.duty_u16(5000)
        speaker.freq(5000)
    else:
        speaker.duty_u16(0)
        speaker.freq(40)