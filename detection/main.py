import requests
from time import sleep
import face_recognition

# from umqtt.simple import MQTTClient
imagePath = r'img3.jpg'


token = ''
payload = {'message' : 'found someone'
          ,'notificationDisabled' : False}

while True :
    img_data = requests.get("http://10.2.6.215/capture").content
    with open('img3.jpg', 'wb') as handler:
        handler.write(img_data)

    image = face_recognition.load_image_file('img3.jpg')
    face_location = face_recognition.face_locations(image)
    if len(face_location)>=1:
        print(f'There are {len(face_location)} faces found.')
        r = requests.post('https://notify-api.line.me/api/notify'
                , headers={'Authorization' : 'Bearer {}'.format(token)}
                , params = payload
                ,files = {'imageFile': open(imagePath, 'rb')})
    sleep(1)
