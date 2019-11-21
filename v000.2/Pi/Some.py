import face_recognition
import picamera
import numpy as np
import json
import paho.mqtt.client as mqtt
import os
import time
from collections import defaultdict

def on_message(client, userdata, message):
	global ux
	ux = str(message.payload)

print('Programm started')

try:
  path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data_file.json')
  os.remove(path)
except:
  print('No data_file, excellent')

camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

print("Loading known face image(s)")
#Init admin photo

users = defaultdict(dict)

with open('data.json','r') as f:
   datastore = json.load(f)

for i in range(len(datastore)):
  some_image = face_recognition.load_image_file(datastore[str(i+1)]['photo_name'])
  some_recog =  face_recognition.face_encodings(some_image)[0]
  some_list = {'name':datastore[str(i+1)]['name'], 'pass': datastore[str(i+1)]['pass'], 'encode': some_recog.tolist()}
  users[i+1] = some_list
with open('data_file.json', 'a') as fedjs:
  json.dump(users, fedjs)

#oleg_image = face_recognition.load_image_file("Oleg.jpg")
#oleg_face_encoding = face_recognition.face_encodings(oleg_image)[0]

#Oleg_list = ['Oleg', oleg_face_encoding.tolist(), Oleg_pass]

#with open('data_file.json', 'w') as write_file:
#  json.dump(Oleg_list[1], write_file)

# Initialize some variables
face_locations = []
face_encodings = []
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

    # Find all the faces and face encodings in the current frame of video

    face_locations = face_recognition.face_locations(output)
    face_encodings = face_recognition.face_encodings(output, face_locations)
    Pass = "null"
    exit = "False"
    ux = "False"

    # Loop over each face found in the frame to see if it's someone we know
    for face_encoding in face_encodings:
     with open('data_file.json', 'r') as feed:
         data = json.load(feed)
        # See if the face is a match for the known face(s
     for i in range(len(data)):
          match = face_recognition.compare_faces([data[str(i+1)]['encode']], face_encoding)
          name = "<Unknown Person>"

          if match[0]:
            name = data[str(i+1)]['name']
            Pass = data[str(i+1)]['pass']

          if (name != "<Unknown Person>"):
                 boolean = "true"
                 print("Recognized ", format(name), "!")
                 print("Accept Throw")
                 client.publish("Accept", boolean)
                 time.sleep(10)
                 print("Pass throw")
                 client.publish("Pass_throw",Pass)
                 while (exit == "False"):
                         client.loop_start()
                         client.subscribe("Pass_check")
                         exit = ux
                         client.loop_stop()
          else:
                  print("I can't see you, or i don't know who are you")


