from chest import inference_only, inference
import cv2
import numpy as np 
from io import BytesIO
import base64

def imagetobase64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
def basetoimage(event):

    im_bytes = base64.b64decode(event["Image"])  # im_bytes is a binary image
    im_file = BytesIO(im_bytes)  # convert image to file-like object
    
    im_data = im_file.read()

    # Decode the image using cv2.imdecode()
    im = cv2.imdecode(np.frombuffer(im_data, np.uint8), cv2.IMREAD_COLOR)

    return im

def lambda_handler(event, context):
    if "Image" in event:
        img = basetoimage(event)
        tuber_or_not = inference_only.inference(img)
        all_chest_disease = inference.inference(img)
        if tuber_or_not == "Tuberculosis":
            result = f"Image is of Tuberculosis patient"
            result_add = "and there is a chance he is suffering from "
            for dis in all_chest_disease:
                result_add = result_add + dis + ","
            if result_add[-1] == ",":
                result = result + result_add[:-1]
        else:
            result = f"There is a chance he is suffering from"
            result_add = " "
            for dis in all_chest_disease:
                result_add = result_add + dis + ","
            if result_add[-1] == ",":
                result = result + result_add[:-1]
        return {
            "Result": result
        }
    