import sys
sys.path.append("hubmap/")
sys.path.append("hubmap/src/")
from hubmap.src.inference import inference
import base64
from PIL import Image
from io import BytesIO
import json 
import pandas as pd 
#import shutil

import os

# def get_model():
#     print("entry")
#     if not os.path.exists('tmp/epoch99step6600.ckpt'):
#         print("does it?")
#         # create an S3 client
#         s3 = boto3.client('s3')
        
#         # specify the bucket name and object key
#         bucket_name = 'mlmodel-t'
#         object_key = 'epoch99step6600.ckpt'
        
#         # specify the local file path to save the downloaded file
#         local_file_path = '/tmp/epoch99step6600.ckpt'
        
#         # get the object from S3
#         s3_object = s3.get_object(Bucket=bucket_name, Key=object_key)
        
#         # download the file to the local file path
#         with open(local_file_path, 'wb') as f:
#             f.write(s3_object['Body'].read())

def basetoimage(event):

    im_bytes = base64.b64decode(event["Image"])  # im_bytes is a binary image
    im_file = BytesIO(im_bytes)  # convert image to file-like object
    
    img = Image.open(im_file)

    img.save('/tmp/10078.tiff')
    update_pd(event["Organ"], img.size)

def imagetobase64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
def update_pd(organ, img_size):
    print(img_size)
    data = {'id': [10078],
        'organ': [organ],
        'data_source': ['Hubmap'],
        'img_height': [img_size[0]],
        'img_width': [img_size[1]],
        'pixel_size': [0.4945],
        'tissue_thickness': [4]}

    df = pd.DataFrame(data)
    df.to_csv("/tmp/test.csv", index= False)



def lambda_handler(event, context):

    if not os.path.exists('/tmp'):
        print("tmp not exist")
        os.mkdir("/tmp")

    if ("Organ" in event):
        basetoimage(event)
        #get_model()
        inference()
        # ans = json.dumps(inference())
        # return {
        #     "Result": ans
        # } 

        return {
            "Result": json.dumps(imagetobase64("/tmp/image.jpg"))
        } 
    #shutil.rmtree("/tmp")    
    return {
        "Result": "wrong input"
    }
# from test import event
# lambda_handler(event, "")

    

