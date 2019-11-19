import face_recognition
import picamera
import numpy as np
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
def on_message(client, userdata, message):
	global ux
	ux = str(message.payload)
	print("Message got ",ux)

camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


while True:
  GPIO.output(18, GPIO.LOW)
  time.sleep(1)
  GPIO.output(18, GPIO.HIGH)
print("Loading known face image(s)")
#Init admin photo
oleg_image = face_recognition.load_image_file("Oleg.jpg")
oleg_face_encoding = face_recognition.face_encodings(oleg_image)[0]
Oleg_pass = "Some_terroble"


#Init user photo
VU_image = face_recognition.load_image_file("V-U.jpg")
VU_face_encoding = face_recognition.face_encodings(VU_image)[0]
VU_pass = "Hi_I_am"

#Init user photo
DA_image = face_recognition.load_image_file("D-A.jpg")
DA_face_encoding = face_recognition.face_encodings(DA_image)[0]
DA_pass = "The_END_IS_COMING"

#Init user photo
Stepa_image = face_recognition.load_image_file("Stepa.jpg")
Stepa_face_encoding=face_recognition.face_encodings(Stepa_image)[0]
Stepa_pass = "212284"

# Initialize some variables
face_locations = []
face_encodings = []
broker_address="192.168.11.1"
print("creating new instance")

client = mqtt.Client("Test_new_stupid_thing")
client.on_message = on_message

print("connecting to broker")
client.connect(broker_address) #connect to broker

Pass = "null"
exit = "False"
ux = "False"

while True:
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
    print("Let's show begins")

    # Find all the faces and face encodings in the current frame of video

    face_locations = face_recognition.face_locations(output)
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know
    for face_encoding in face_encodings:

        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([oleg_face_encoding], face_encoding)
        match1 = face_recognition.compare_faces([VU_face_encoding], face_encoding)
        match2 = face_recognition.compare_faces([DA_face_encoding], face_encoding)
        match4 = face_recognition.compare_faces([Stepa_face_encoding], face_encoding)

        name = "<Unknown Person>"

        if match[0]:
         name = "Oleg"
         Pass = Oleg_pass
        if match1[0]:
         name = "V.U."
         Pass = VU_pass
        if match2[0]:
         name = "D.A."
         Pass = DA_pass
        if match4[0]:
         name = "Stepa"
         Pass = Stepa_pass


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


