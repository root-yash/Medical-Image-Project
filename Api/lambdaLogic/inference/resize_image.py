from PIL import Image

image = Image.open("tmp/10078.tiff")
new_image = image.resize((1000,1000), resample= Image.LANCZOS)
new_image.save('tmp/100783.tiff')

