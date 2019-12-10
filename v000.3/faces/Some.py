import face_recognition
import picamera
import numpy as np
import json
import paho.mqtt.client as mqtt
import os
import time
from collections import defaultdict
from RPi import GPIO

#Function, that called, then message recevied
def on_message(client, userdata, message):
	global ux
	ux = str(message.payload)

print('Programm started')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, True)
time.sleep(1/2)
GPIO.output(18, False)
time.sleep(1/2)

GPIO.output(18, True)
time.sleep(1/2)
GPIO.output(18, False)
time.sleep(1/2)

ux = "False"

#Deleting database
try:
  path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data_file.json')
  os.remove(path)
except:
  print('No data_file, excellent')

#Camera calibration
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

print("Loading known face image(s)")

GPIO.output(18, True)
time.sleep(1/5)
GPIO.output(18, False)
time.sleep(1/5)

GPIO.output(18, True)
time.sleep(1/5)
GPIO.output(18, False)
time.sleep(1/5)

#Init photos
users = defaultdict(dict)

with open('data.json','r') as f:
   datastore = json.load(f)
#Loading database, and creating new damp database
for i in range(len(datastore)):
  some_image = face_recognition.load_image_file(datastore[str(i+1)]['photo_name'])
  some_recog =  face_recognition.face_encodings(some_image)[0]
  some_list = {'name':datastore[str(i+1)]['name'], 'pass': datastore[str(i+1)]['pass'], 'encode': some_recog.tolist()}
  users[i+1] = some_list
  GPIO.output(18, True)
  time.sleep(1/3)
  GPIO.output(18, False)
  time.sleep(1/3)
with open('data_file.json', 'a') as fedjs:
  json.dump(users, fedjs)

# Initialize some variables
face_locations = []
face_encodings = []

GPIO.output(18, True)
time.sleep(1/6)
GPIO.output(18, False)
time.sleep(1/6)

GPIO.output(18, True)
time.sleep(1/6)
GPIO.output(18, False)
time.sleep(1/6)

#Creating mqtt connection
broker_address="192.168.11.1"
print("creating new instance")

client = mqtt.Client("Test_new_stupid_thing")
client.on_message = on_message

print("connecting to broker")
client.connect(broker_address) #connect to broker

while True:
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
    print("Let's show begins")

    GPIO.output(18, True)
    time.sleep(1/10)
    GPIO.output(18, False)
    time.sleep(1/10)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    face_encodings = face_recognition.face_encodings(output, face_locations)

    Pass = "null"
    exit = "False"

    # Loop over each face found in the frame to see if it's someone we know
    for face_encoding in face_encodings:
     with open('data_file.json', 'r') as feed:
         data = json.load(feed)
        # See if the face is a match for the known faces
     for i in range(len(data)):
          match = face_recognition.compare_faces([data[str(i+1)]['encode']], face_encoding)
          name = "<Unknown Person>"

          if match[0]:
            name = data[str(i+1)]['name']
            Pass = data[str(i+1)]['pass']

          if (name != "<Unknown Person>"):
                 boolean = "true"
                 print("Recognized ", format(name), "!")
                 print("Name throw")
                 client.publish("Users_name", name)
                 print("Message waiting")
                 while (exit != "b'1'"):
                         client.loop_start()
                         client.subscribe("Message_check")
                         exit = ux
                         client.loop_stop()
                 print ("Pass throw")
                 time.sleep(1/6)
                 client.publish("Pass_throw", Pass)
                 while (exit != "b'True'"):
                         client.loop_start()
                         client.subscribe("Pass_check")
                         exit = ux
                         client.loop_stop()
          else:
             print("I can't recognized it")
          client.unsubscribe("Message_check")
          client.unsubscribe("Pass_check")

