from tensorflow.keras.models import load_model
import numpy as np 
import cv2
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

def get_inference(img):
    # Load the model from the .h5 file
    model = load_model('model/EfficientNetB3-leukemia-0.97.h5')
    
    img=cv2.resize(img, (300, 300))
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)            
    prediction = model.predict(np.expand_dims(img, axis=0))
    return np.argmax(prediction[0])

def lambda_handler(event, context):
    # event = {}
    # event["Image"] = imagetobase64("testing/leukaemia/UID_H10_100_1_hem.bmp")
    if "Image" in event:
        image = basetoimage(event)
        prediction = get_inference(image)
        if prediction == 0:
            return {
                "Result": "Image is of Leukaemia cell"
            }
        else:
            return {
                "Result": "Image is of Normal cell"
            }
# print(lambda_handler("", ""))