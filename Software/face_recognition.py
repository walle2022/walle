#!/usr/bin/env python3

import cv2
import numpy as np
import os 

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=960,
    display_height=540,
    framerate=21,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=True"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def face_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('/home/wall-e/Documents/trainer/trainer.yml')
#cascadePath = "haarcascade_frontalface_default.xml"
#faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades+cascadePath);
    face_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
    font = cv2.FONT_HERSHEY_SIMPLEX

    #initiate id counter
    id = 0
    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'Josh', 'Greg', 'Lianna', 'Divya', 'W'] 
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
#cam.set(3, 640) # set video widht
#cam.set(4, 480) # set video height
# Define min window size to be recognized as a face
#minW = 0.1*cam.get(3)
#minH = 0.1*cam.get(4)
#print(cam.isOpened())
    if cam.isOpened():
        try:
            cv2.namedWindow("Face Recognizer", cv2.WINDOW_AUTOSIZE)
            while True:
                ret, img =cam.read()
                img = cv2.flip(img, -1) # Flip vertically
                #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
                faces = faceCascade.detectMultiScale(gray,1.3,5)
                for(x,y,w,h) in faces:
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                    id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
                    # If confidence is less them 100 ==> "0" : perfect match 
                    if (confidence < 100):
                        id = names[id]
                        confidence = "  {0}%".format(round(100 - confidence))
                    else:
                        id = "unknown"
                        confidence = "  {0}%".format(round(100 - confidence))
        
                    cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255),2)
                    cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
                cv2.imshow('camera',img) 
                k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                if k == 27:
                    break
        finally:
            # Do a bit of cleanup
            print("\n [INFO] Exiting Program and cleanup stuff")
            cam.release()
            cv2.destroyAllWindows()
    else: 
        print("Unable to open camera")

if __name__ == "__main__":
    face_recognizer()

