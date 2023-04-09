from pathlib import Path
KAGGLE_DIR = "/tmp"

INPUT_DIR = "/tmp"
OUTPUT_DIR = "/tmp"


COMPETITION_DATA_DIR = "/tmp"


TRAIN_PREPARED_CSV_PATH = "train_prepared.csv"
VAL_PRED_PREPARED_CSV_PATH = "val_pred_prepared.csv"
TEST_PREPARED_CSV_PATH = "/tmp/test_prepared.csv"

N_SPLITS = 4
RANDOM_SEED = 2022
SPATIAL_SIZE = 768
VAL_FOLD = 0
NUM_WORKERS = 2
BATCH_SIZE = 4
MODEL = "unet"
LOSS = "dice"
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 0.0
FAST_DEV_RUN = False
GPUS = 1
MAX_EPOCHS = 90
PRECISION = 16
DEBUG = False
BACKBONE = 'efficientnet-b5'

DEVICE = "cpu"
THRESHOLD = 0.5

def rgb2hex(rgb_tuple):
    r,g,b = rgb_tuple
    def clamp(x): 
        return max(0, min(x, 255))
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))

ORGANS = ['kidney', 'largeintestine', 'lung', 'prostate', 'spleen']
_COLOURS = [(230, 0, 73), (11, 180, 255), (80, 233, 145), (230, 216, 0), (155, 25, 245)]
O2C_MAP = {_o:_c for _o,_c in zip(ORGANS, _COLOURS)}
O2C_HEX_MAP = {_o:rgb2hex(_c) for _o,_c in O2C_MAP.items()}

FINAL_IMAGE = "/tmp/image.jpg"