from utils import prepare_data
from config import COMPETITION_DATA_DIR, N_SPLITS, RANDOM_SEED, TEST_PREPARED_CSV_PATH, SPATIAL_SIZE, VAL_FOLD, NUM_WORKERS
from lightning_datamodule import LitDataModule
import numpy as np 
import monai 
import torch 
from model import LitModule
from tqdm import tqdm 
from config import DEVICE, THRESHOLD
import pandas as pd 
from pathlib import Path
from ready_image import examine_id
import os 

def mask2rle(img):
    '''
    Efficient implementation of mask2rle, from @paulorzp
    --
    img: numpy array, 1 - mask, 0 - background
    Returns run length as string formated
    Source: https://www.kaggle.com/xhlulu/efficient-mask2rle
    '''
    pixels = img.T.flatten()
    pixels = np.pad(pixels, ((1, 1), ))
    runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
    runs[1::2] -= runs[::2]
    return ' '.join(str(x) for x in runs)


@torch.no_grad()
def create_pred_df(module, dataloader, threshold):
    ids = []
    rles = []
    for batch in dataloader:
        print("done")
        id_ = batch["id"].numpy()[0]
        height = batch["img_height"].numpy()[0]
        width = batch["img_width"].numpy()[0]
        
        images = batch["image"].to(module.device)
        outputs = module(images)[0]
        
        post_pred_transform = monai.transforms.Compose(
            [
                monai.transforms.Resize(spatial_size=(height, width), mode="nearest"),
                monai.transforms.Activations(sigmoid=True),
                monai.transforms.AsDiscrete(threshold=threshold),
            ]
        )
        
        mask = post_pred_transform(outputs).to(torch.uint8).cpu().detach().numpy()[0]
        
        rle = mask2rle(mask)
        
        ids.append(id_)
        rles.append(rle)
        
    return pd.DataFrame({"id": ids, "rle": rles})


def infer(
    checkpoint_path: str,
    device: str = DEVICE,
    test_csv_path: str = TEST_PREPARED_CSV_PATH,
    spatial_size: int = SPATIAL_SIZE,
    num_workers: int = NUM_WORKERS,
    threshold: float = THRESHOLD,
):
    module = LitModule.load_eval_checkpoint(checkpoint_path, device)

    data_module = LitDataModule(
        test_csv_path=TEST_PREPARED_CSV_PATH,
        spatial_size=spatial_size,
        val_fold=0,
        batch_size=1,
        num_workers=0,
    )
    data_module.setup()

    test_dataloader = data_module.test_dataloader()
    
    test_pred_df = create_pred_df(module, test_dataloader, threshold)
    
    return test_pred_df

def inference():

    test_df = prepare_data(COMPETITION_DATA_DIR, "test", N_SPLITS, RANDOM_SEED)
    nrows = 1

    data_module = LitDataModule(
        test_csv_path=TEST_PREPARED_CSV_PATH,
        spatial_size=SPATIAL_SIZE,
        val_fold=VAL_FOLD,
        batch_size=nrows ** 2,
        num_workers=NUM_WORKERS,
    )

    data_module.setup()
    checkpoint_path = list(Path("model/").glob("*.ckpt"))[0]

    test_pred_df = infer(checkpoint_path)
    test_pred_df =  test_pred_df[0:1]
    test_original = test_df[test_df.id == test_pred_df.id[0]]
    test_pred = test_original.copy()
    test_pred["rle"] = test_pred_df.rle[0]
    #return test_pred["rle"].tolist()
    examine_id(test_pred, ex_id = None, plot_overlay=True, plot_original=False, plot_segmentation=False)

