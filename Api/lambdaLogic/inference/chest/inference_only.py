from tensorflow.keras.models import load_model
import cv2
import numpy as np
import cv2


def inference(img):
    test_data = []
    img = cv2.resize(img, (28,28))
    if img.shape[2] ==1:
        img = np.dstack([img, img, img])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img=np.array(img)
    img = img/255

    loaded_model = load_model('model/my_model1/')
    result = loaded_model.predict(np.expand_dims(img, axis=0)).tolist()[0]
    if result[0]<result[1]:
        return "Tuberculosis"
    else:
        return "Normal"
