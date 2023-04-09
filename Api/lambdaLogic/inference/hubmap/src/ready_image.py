import numpy as np
import json 

from matplotlib import pyplot as plt
from config import O2C_MAP, ORGANS, _COLOURS, FINAL_IMAGE


import tensorflow as tf
import tensorflow_io as tfio
import cv2
from matplotlib.patches import Rectangle

def rle_decode(mask_rle, shape, color=1):
    """ TBD
    
    Args:
        mask_rle (str): run-length as string formated (start length)
        shape (tuple of ints): (height,width) of array to return 
    
    Returns: 
        Mask (np.array)
            - 1 indicating mask
            - 0 indicating background

    """
    # Split the string by space, then convert it into a integer array
    s = np.array(mask_rle.split(), dtype=int)

    # Every even value is the start, every odd value is the "run" length
    starts = s[0::2] - 1
    lengths = s[1::2]
    ends = starts + lengths

    # The image image is actually flattened since RLE is a 1D "run"
    if len(shape)==3:
        h, w, d = shape
        img = np.zeros((h * w, d), dtype=np.float32)
    else:
        h, w = shape
        img = np.zeros((h * w,), dtype=np.float32)

    # The color here is actually just any integer you want!
    for lo, hi in zip(starts, ends):
        img[lo : hi] = color
        
    # Don't forget to change the image back to the original shape
    return img.reshape(shape).T


def rle_decode_top_to_bot_first(mask_rle, shape):
    """ TBD
    
    Args:
        mask_rle (str): run-length as string formated (start length)
        shape (tuple of ints): (height,width) of array to return 
    
    Returns:
        Mask (np.array)
            - 1 indicating mask
            - 0 indicating background

    """
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(shape[0]*shape[1], dtype=np.uint8)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = 1
    return img.reshape((shape[1], shape[0]), order='F').T  # Reshape from top -> bottom first


def rle_encode(img):
    """ TBD
    
    Args:
        img (np.array): 
            - 1 indicating mask
            - 0 indicating background
    
    Returns: 
        run length as string formated
    """
    pixels = img.T.flatten()
    pixels = np.concatenate([[0], pixels, [0]])
    runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
    runs[1::2] -= runs[::2]
    return ' '.join(str(x) for x in runs)

def flatten_l_o_l(nested_list):
    """ Flatten a list of lists """
    return [item for sublist in nested_list for item in sublist]

def load_json_to_dict(json_path):
    """ tbd """
    with open(json_path) as json_file:
        data = json.load(json_file)
    return data

def tf_decode_tiff(img_path, to_numpy=False, to_rgb=False):
    img = tf.io.read_file(img_path)
    img = tfio.experimental.image.decode_tiff(img)
    
    # Optionals
    if to_rgb: img = tfio.experimental.color.rgba_to_rgb(img)
    if to_numpy: img = img.numpy()
        
    return img

def get_overlay(img_path, organ, rle_str, img_shape, _alpha=0.999, _beta=0.35, _gamma=0):
    _img = tf_decode_tiff(img_path, to_numpy=True, to_rgb=True).astype(np.float32)
    _seg_rgb = (np.stack([rle_decode(rle_str, shape=img_shape, color=1),]*3, axis=-1)*O2C_MAP[organ]).astype(np.float32)
    seg_overlay = cv2.addWeighted(src1=_img, alpha=_alpha, 
                                  src2=_seg_rgb, beta=_beta, gamma=_gamma)
    return seg_overlay/255.

def examine_id(df, ex_id = None, plot_overlay=True, plot_original=False, plot_segmentation=False, _figsize=(20,20)):
    """ Wrapper function to allow for easy visual exploration of an example """
    
    demo_ex = df
    
    if ex_id is None:
        ex_id = df["id"].sample(1).values[0]
    
    demo_ex = df[df["id"]==ex_id].squeeze()

    print(f"\n\n... IMAGE WITH RGB SEGMENTATION MASK OVERLAY ({demo_ex['organ']}) ...\n")
    seg_overlay = get_overlay(demo_ex.image, demo_ex.organ, demo_ex.rle, img_shape=(demo_ex.img_width, demo_ex.img_height))

    plt.figure(figsize=_figsize)
    plt.imshow(seg_overlay)
    plt.title(f"Segmentation Overlay id=`{ex_id}` (organ=`{demo_ex['organ']}`)", fontweight="bold")
    handles = [Rectangle((0,0),1,1, color=(*[__c/255. for __c in _c], 0.5)) for _c in _COLOURS]
    labels = ORGANS
    plt.legend(handles,labels)
    plt.axis(False)
    plt.savefig(FINAL_IMAGE, )

    print("\n\n... SINGLE ID EXPLORATION FINISHED ...\n\n")