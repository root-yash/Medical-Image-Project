from PIL import Image
import os 
all_tiff = os.listdir("testing/hubmap")
for i in all_tiff:
    image = Image.open("testing/hubmap/"+i)
    new_image = image.resize((1000,1000), resample= Image.LANCZOS)
    new_image.save("testing/hubmap/"+i)

