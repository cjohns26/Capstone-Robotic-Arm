import subprocess
from pathlib import Path
import cv2
import PIL
from PIL import Image
import torch
import torchvision.transforms as transforms
import tensorflow as tf
from keras.models import load_model
import numpy as np
import pandas as pd
import mysql.connector
import mysql
import time
import xarm

arm = xarm.Controller('USB')
def main():
    transactionID = int(getID()) +1
    croppedImagePath = takePic(transactionID)
    classification = classify(croppedImagePath)
    insertRecord(classification, "THIS")
    vec = predictImg(croppedImagePath)
    print(f"YESSSSS: {vec}")
    attemptGrab(vec)
    
    

   
    

def classify(imgPath):
    detect_path = 'C:\\Users\\Blake\\OneDrive\\Desktop\\MasterFolder\\yolov7\\detect.py'
    source_arguments = '--source'
    weight_arguments = '--weights'
    try:
       #load detect model
       result =  subprocess.run(['python', detect_path, weight_arguments, 'C:\\Users\\Blake\\OneDrive\\Desktop\\MasterFolder\\yolov7\\best.pt', source_arguments, imgPath], check=True, capture_output=True)
       #get standard output from subprocess
       yolo_output = result.stdout
       #clean up the output string
       myString = str(yolo_output)
       ending = myString.split(',')
       finalString = ending[17].split(' ')
       classification = finalString[len(finalString)-1]
       print(f"Classification: {classification}")
    except subprocess.CalledProcessError as e:
         print(f'An error occurred: {e}')

    return classification

    
def takePic(picID):
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    # Capture a frame from the camera
    ret, frame = cap.read()
    # Save the captured frame as an image
    save_path = "C:\\Users\\Blake\\OneDrive\\Desktop\\MasterFolder"
    
    if ret:
        captured_path = f"{save_path}/captured_ball_{(picID)}.jpg"
        crooped_path = f"{save_path}/cropped_ball_{(picID)}.jpg"
        box = (165,97,373,340)
        cv2.imwrite(captured_path, frame)
        img = Image.open(captured_path)
        img2 = img.crop(box)
        img2.save(crooped_path)
        print(f"Image cropped and saved as {crooped_path}")
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
    return crooped_path


def insertRecord(classification, filepath):
    host = "172.16.2.161"
    port = 37306
    user = "capstone"
    password = "UAPass50!"
    database ="capstone"
    table = "TRANSACTIONS"

    try:
        connection = mysql.connector.connect(
            host = host,
            user = user,
            port = port,
            password = password,
            database = database
        )
        cursor = connection.cursor()
        query = f"INSERT INTO TRANSACTIONS(classification, image_filepath, session_id) VALUES('{classification}', '{filepath}', '1')"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close


    except Exception as e:
        print(f"Error in sql: {e}")    
def getID():
    host = "172.16.2.161"
    port = 37306
    user = "capstone"
    password = "UAPass50!"
    database ="capstone"
   

    try:
        connection = mysql.connector.connect(
            host = host,
            user = user,
            port = port,
            password = password,
            database = database
        )
        cursor = connection.cursor()
        query = f"SELECT max(transaction_id) FROM TRANSACTIONS"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        connection.close
        return result


    except Exception as e:
        print(f"Error in sql: {e}")    

def load_and_preprocess_image(image_path, target_size=(224,224), keep_aspect_ratio=False):
  img = tf.keras.utils.load_img(image_path,
                                target_size=target_size,
                                keep_aspect_ratio=keep_aspect_ratio)
  return tf.keras.utils.img_to_array(img)

def predictImg(image):
    motor_6_path = 'motor_6.h5' #change to correct path
    motor_6 = load_model(motor_6_path)
    motor_5_path = 'motor_5.h5' #change to correct path
    motor_5 = load_model(motor_5_path)
    motor_4_path = 'motor_4.h5' #change to correct path
    motor_4 = load_model(motor_4_path)
    motor_3_path = 'motor_3.h5' #change to correct path
    motor_3 = load_model(motor_3_path)
    image_path = image

    image = np.array([load_and_preprocess_image(image_path) / 255])
    pos6 = motor_6.predict(image)
    pos5 = motor_5.predict(image)
    pos4 = motor_4.predict(image)
    pos3 = motor_3.predict(image)

    motor_vec = (pos6,pos4,pos3,pos5)

    return motor_vec

# Arm Code ---------------

def attemptGrab(vec):

    six = int(vec[0])
    four = int(vec[1])
    three = int(vec[2])
    five = int(vec[3])
    two = 1500
    one = 2250

    servo1 = xarm.Servo(1, 1500)
    servo2 = xarm.Servo(2, 1500)
    servo3 = xarm.Servo(3, 1500)
    servo4 = xarm.Servo(4, 1500)
    servo5 = xarm.Servo(5, 1500)
    servo6 = xarm.Servo(6, 1500)
    

    arm.setPosition(6, six)
    time.sleep(1)
    arm.setPosition(2, two)
    time.sleep(1)
    arm.setPosition(4,four)
    time.sleep(1)
    arm.setPosition(3, three)
    time.sleep(1)
    arm.setPosition(5, five)
    time.sleep(1)
    grab(one) 
    time.sleep(2)
    drop()
    time.sleep(1)
    resetArm()
   

def resetArm():
    arm.setPosition(5, 1500)
    time.sleep(1)
    arm.setPosition(4, 1500)
    time.sleep(1)
    arm.setPosition(3, 1500)
    time.sleep(1)
    arm.setPosition(2, 1500)
    time.sleep(1)
    arm.setPosition(6, 1500)
    
def drop():
    arm.setPosition(5, 1330)
    time.sleep(1)
    arm.setPosition(6, 500)
    time.sleep(1)
    arm.setPosition(4,1100)
    time.sleep(1)
    release()

def release():
    arm.setPosition(1, 1500)

def grab(pos):
    arm.setPosition(1, pos)







main()