# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
oleg_image = face_recognition.load_image_file("Oleg.jpg")
oleg_face_encoding = face_recognition.face_encodings(oleg_image)[0]

VU_image = face_recognition.load_image_file("V-U.jpg")
VU_face_encoding = face_recognition.face_encodings(VU_image)[0]

DA_image = face_recognition.load_image_file("D-A.jpg")
DA_face_encoding = face_recognition.face_encodings(DA_image)[0]

Stepa_image = face_recognition.load_image_file("Stepa.jpg")
Stepa_face_encoding = face_recognition.face_encodings(Stepa_image)[0]


# Initialize some variables
face_locations = []
face_encodings = []

print("Let's show begins")

while True:
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([oleg_face_encoding], face_encoding)
        match1 = face_recognition.compare_faces([VU_face_encoding], face_encoding)
        match2 = face_recognition.compare_faces([DA_face_encoding], face_encoding)
        match4 = face_recognition.compare_faces([Stepa_face_encoding], face_encoding)
        name = "<Unknown Person>"

        if match[0]:
            name = "Oleg"
        if match1[0]:
           name = "V.U."
        if match2[0]:
            name = "D.A."
        if match4[0]:
            name = "Stepa"

        print("I see someone named {}!".format(name))


