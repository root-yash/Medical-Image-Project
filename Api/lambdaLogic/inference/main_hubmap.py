import sys
sys.path.append("hubmap/")
sys.path.append("hubmap/src/")
from inference import inference
import base64
from PIL import Image
from io import BytesIO
import json 
import pandas as pd 

def basetoimage(base):
    im_bytes = base64.b64decode(base)  # im_bytes is a binary image
    im_file = BytesIO(im_bytes)  # convert image to file-like object
    img = Image.open(im_file)
    img.save('hubmap/temp/input/hubmap-organ-segmentation/test_images/10078.tiff')

def imagetobase64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
def update_pd(organ):
    df = pd.read_csv("hubmap/temp/input/hubmap-organ-segmentation/test.csv")
    df.loc[:, 'organ'] = organ
    df.to_csv("hubmap/temp/input/hubmap-organ-segmentation/test.csv", index= False)
    
def lambda_handler(event, context):
    if ("organ" in event):
        basetoimage(event["Image"])
        update_pd(event["Organ"])

        inference()

        return {
            "Result": json.dumps(imagetobase64("hubmap/temp/image.jpg"))
        }     
    return {
        "Result": "wrong input"
    }

    

