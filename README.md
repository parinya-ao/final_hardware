# The privalazy Door

## ที่มาและแนวคิดการออกแบบ

โครงงานนี้เริ่มต้นมาจากปัญหาของเด็กหอที่อยู่หอกับเพื่อนๆแล้วต้องคอยลุกไปเปิดประตูให้เพื่อนเพราะล็อคห้องไว้(ไม่ล็อคก็กลัวอันตราย) ทางกลุ่มเราจึงคิดค้นระบบล็อคประตูที่มีความปลอดภัย ประกอบด้วย3ฟังก์ชัน คือ \
1.ใส่รหัส \
2.แตะคีย์การ์ด \
3.กดปลดล็อคผ่านสมาร์ทโฟน หากเราจะปลดล็อคประตูผ่านสมาร์ทโฟน แล้วกลัวว่าคนที่เคาะประตูนั้นไม่ใช่เพื่อนของเรา เรามีระบบกล้องจับภาพคนเคาะประตูที่สามารถดูได้ผ่านสมาร์ทโฟนแบบrealtime 

## **รายการอุปกรณ์ที่ใช้**
1. Board ESP32 S3 devmodule (2)
2. ESP32 camera module (1)
3. ITEAD PN532 NFC RFID module set (1)
4. 4x3 Matrix Keypad Module
5. OLED (1)
6. SG90 Micro Servo (1)
7. Buzzer (1)


## libraries

### Python
- face_recognition
- requests
- time
- machine
- hashlib
- ssd1306
- network
- servo
- umqtt.simple

### C
- esp_camera
- camera_pins
- WiFi
- PubSubClient
- Wire
- PN532_I2C
- PN532
- NfcAdapter

# File
<pre>
final_hardware
│   .gitignore 
│   LICENSE #
│   node_red_flows.json
│   OverAll.png
│   README.md
│
├───camera #code on board esp32 wrover camera
│       .skip.esp32c3
│       .skip.esp32c6
│       .skip.esp32h2
│       app_httpd.cpp
│       camera_index.h # c/c++ code about sever (HTML file to gzip ) for camera
│       camera_pins.h #define GPIO
│       main.ino #main code
│       partitions.csv #partitions table
│
├───circuit
│       circuit_MAIN.pdf # overall circuit for main board
│       circuit_NFC.pdf # overall circuit for board that connect with NFC
│
├───detection # python code for face detection 
│       main.py
│
├───main # code of main board (micropython)
│   │   .DS_Store
│   │   config.py #config for conect mqtt
│   │   main.py #main code
│   │
│   └───lib
│       │   .DS_Store
│       │   ssd1306.py #library for OLED
│       │
│       └───servo # Library for servo
│               __init__.py
│               __main__.py
│
└───NFC # code .ion for board to control nfc
        config.h #config for mqtt conection
        main.ino # main code
</pre>

## Node-red
### flow
![image](https://github.com/parinya-ao/final_hardware/assets/159911463/89855bb3-d5a1-4197-a8f4-a7f79329085d)


### ui
![image](https://github.com/parinya-ao/final_hardware/assets/159911463/91988040-0d57-4a0a-8419-91130cd87515)


## จัดทำโดย 4 ยอดกุมาร (CPE37, KU83)
นาย ชานน ลีดี 6610505349\
นาย กฤษกร สุทธิรักษ์ 6610501971\
นาย ปริญญา อบอุ่น 6610502145\
นาย ไทยเงิน ปินตา 6610502030

โครงการนี้เป็นส่วนหนึ่งของวิชา 01204114 Introduction to Hardware Development ภาคเรียนที่ 2/2023
ภาควิชาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์
