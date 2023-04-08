from typing import Any
from typing import Callable
from typing import Dict
from typing import Tuple

import monai
import numpy as np
import pandas as pd
import pytorch_lightning as pl
import tifffile

from monai.data import CSVDataset
from monai.data import DataLoader
from monai.data import ImageReader


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

class TIFFImageReader(ImageReader):
    def read(self, data: str) -> np.ndarray:
        image = tifffile.imread(data)
        image = rgb2gray(image)
        return image

    def get_data(self, img: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        return img, {"spatial_shape": np.asarray(img.shape), "original_channel_dim": -1}

    def verify_suffix(self, filename: str) -> bool:
        return ".tiff" in filename
    

class LitDataModule(pl.LightningDataModule):
    def __init__(
        self,
        test_csv_path: str,
        spatial_size: int,
        val_fold: int,
        batch_size: int,
        num_workers: int,
    ):
        super().__init__()

        self.save_hyperparameters()

        self.test_df = pd.read_csv(test_csv_path)

        self.test_transform = self._init_transforms()
        
    def _init_transforms(self):
        spatial_size = (self.hparams.spatial_size, self.hparams.spatial_size)
        print(spatial_size)
        test_transform = monai.transforms.Compose(
            [
                monai.transforms.LoadImaged(keys=["image"], reader=TIFFImageReader),
                monai.transforms.AddChanneld(keys=["image"]),
                monai.transforms.ScaleIntensityd(keys=["image"]),
                monai.transforms.Resized(keys=["image"], spatial_size=spatial_size, mode="nearest"),
                monai.transforms.ToTensord(keys=["image"]),
            ]
        )

        return test_transform

    def setup(self, stage: str = None):
          self.test_dataset = self._dataset(self.test_df, transform=self.test_transform)

    def _dataset(self, df: pd.DataFrame, transform: Callable) -> CSVDataset:
        print("df")
        return CSVDataset(src=df, transform=transform)

    def test_dataloader(self) -> DataLoader:
        print("test")
        return self._dataloader(self.test_dataset)

    def _dataloader(self, dataset: CSVDataset) -> DataLoader:
        print("hiiiiiiiiiiiiii")
        return DataLoader(
            dataset,
            batch_size=self.hparams.batch_size,
            shuffle=False,
            num_workers=self.hparams.num_workers,
            pin_memory=True,
        )