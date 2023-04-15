import tensorflow as tf

import numpy as np
import pydicom
import cv2
import base64
from io import BytesIO

import tensorflow as tf

margin = 0.6
theta = lambda t: (K.sign(t)+1.)/2.

TYPES = ["FLAIR", "T1w", "T2w", "T1wCE"]
WHITE_THRESHOLD = 10 # out of 255
EXCLUDE = [109, 123, 709]


def imagetobase64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string

def load_dicom(event, size = 128):
    ''' 
    Reads a DICOM image, standardizes so that the pixel values are between 0 and 1, then rescales to 0 and 255
    
    Note super sure if this kind of scaling is appropriate, but everyone seems to do it. 
    '''
    im_bytes = base64.b64decode(event["Image"]) 
    im_file = BytesIO(im_bytes)  

    dicom = pydicom.dcmread(im_file)
    data = dicom.pixel_array
    if np.max(data) != 0:
        data = data / np.max(data)
    data = (data * 255).astype(np.uint8)
    return cv2.resize(data, (size, size))

def loss(y_true, y_pred):
    return - (1 - theta(y_true - margin) * theta(y_pred - margin)
                - theta(1 - margin - y_true) * theta(1 - margin - y_pred)
             ) * (y_true * K.log(y_pred + 1e-8) + (1 - y_true) * K.log(1 - y_pred + 1e-8))

def mish(inputs):
    x = tf.nn.softplus(inputs)
    x = tf.nn.tanh(x)
    x = tf.multiply(x, inputs)
    return x

def lambda_handler(event, context):
    if "Image" in event:
        images = load_dicom(event)
        model_best = tf.keras.models.load_model(filepath="model/best_model0.747.h5",custom_objects={"loss":loss,'leaky_relu': tf.nn.leaky_relu,'mish':mish})
        y_pred = model_best.predict(np.expand_dims(images, axis=0))
        if y_pred[0][0]>y_pred[0][1]:
            return {
                "Result": "This does not contain malignant tumor"
            }
        else:
            return {
                "Result": "This does contains malignant tumor"
            }