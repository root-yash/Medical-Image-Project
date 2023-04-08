from monai.data import ImageReader
import tifffile
from typing import Dict
from typing import Tuple
import numpy as np 
from typing import Any
import pandas as pd 
import pytorch_lightning as pl 
import monai
from typing import Callable
from monai.data import DataLoader
from monai.data import CSVDataset


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
        train_csv_path: str,
        test_csv_path: str,
        spatial_size: int,
        val_fold: int,
        batch_size: int,
        num_workers: int,
    ):
        super().__init__()

        self.save_hyperparameters()

        self.train_df = pd.read_csv(train_csv_path)
        self.test_df = pd.read_csv(test_csv_path)

        self.train_transform, self.val_transform, self.test_transform = self._init_transforms()
        
    def _init_transforms(self) -> Tuple[Callable, Callable, Callable]:
        spatial_size = (self.hparams.spatial_size, self.hparams.spatial_size)
        train_transform = monai.transforms.Compose(
            [
                monai.transforms.LoadImaged(keys=["image"], reader=TIFFImageReader),
                monai.transforms.AddChanneld(keys=["image"]),
                monai.transforms.ScaleIntensityd(keys=["image"]),
                monai.transforms.LoadImaged(keys=["mask"]),
                monai.transforms.AddChanneld(keys=["mask"]),
                monai.transforms.RandFlipd(keys=["image", "mask"], prob=0.5, spatial_axis=0),
                monai.transforms.RandFlipd(keys=["image", "mask"], prob=0.5, spatial_axis=1),
                monai.transforms.RandRotate90d(keys=["image", "mask"], prob=0.75, spatial_axes=(0, 1)),
                monai.transforms.OneOf(
                    [
                        #monai.transforms.RandGaussianNoised(keys=["image"], prob=1.0, std=0.1),
                        monai.transforms.RandAdjustContrastd(keys=["image"], prob=1.0, gamma=(0.5, 4.5)),
                        monai.transforms.RandShiftIntensityd(keys=["image"], prob=1.0, offsets=(0.1, 0.2)),
                        monai.transforms.RandHistogramShiftd(keys=["image"], prob=1.0),
                    ]
                ),
                monai.transforms.OneOf(
                    [
                        monai.transforms.RandGridDistortiond(keys=["image", "mask"], prob=0.5, distort_limit=0.2),
                        #monai.transforms.RandZoomd(keys=["image", "mask"], prob=0.5, spatial_size=spatial_size,  mode="nearest"),

                    ]
                ),
                monai.transforms.Resized(keys=["image", "mask"], spatial_size=spatial_size, mode="nearest"),
                monai.transforms.ToTensord(keys=["image", "mask"]),
            ]
        )

        val_transform = monai.transforms.Compose(
            [
                monai.transforms.LoadImaged(keys=["image"], reader=TIFFImageReader),
                monai.transforms.AddChanneld(keys=["image"]),
                monai.transforms.ScaleIntensityd(keys=["image"]),
                monai.transforms.LoadImaged(keys=["mask"]),
                monai.transforms.AddChanneld(keys=["mask"]),
                #monai.transforms.RandZoomd(keys=["image", "mask"], prob=0.5, spatial_size=spatial_size,  mode="nearest"),
                monai.transforms.Resized(keys=["image", "mask"], spatial_size=spatial_size, mode="nearest"),
                monai.transforms.ToTensord(keys=["image", "mask"]),
            ]
        )

        test_transform = monai.transforms.Compose(
            [
                monai.transforms.LoadImaged(keys=["image"], reader=TIFFImageReader),
                monai.transforms.AddChanneld(keys=["image"]),
                monai.transforms.ScaleIntensityd(keys=["image"]),
                monai.transforms.Resized(keys=["image"], spatial_size=spatial_size, mode="nearest"),
                monai.transforms.ToTensord(keys=["image"]),
            ]
        )

        return train_transform, val_transform, test_transform

    def setup(self, stage: str = None):
        if stage == "fit" or stage is None:
            train_df = self.train_df[self.train_df.fold != self.hparams.val_fold].reset_index(drop=True)
            val_df = self.train_df[self.train_df.fold == self.hparams.val_fold].reset_index(drop=True)

            self.train_dataset = self._dataset(train_df, transform=self.train_transform)
            self.val_dataset = self._dataset(val_df, transform=self.val_transform)

        if stage == "test" or stage is None:
            self.test_dataset = self._dataset(self.test_df, transform=self.test_transform)

    def _dataset(self, df: pd.DataFrame, transform: Callable) -> CSVDataset:
        return CSVDataset(src=df, transform=transform)

    def train_dataloader(self) -> DataLoader:
        return self._dataloader(self.train_dataset, train=True)

    def val_dataloader(self) -> DataLoader:
        return self._dataloader(self.val_dataset)

    def test_dataloader(self) -> DataLoader:
        return self._dataloader(self.test_dataset)

    def _dataloader(self, dataset: CSVDataset, train: bool = False) -> DataLoader:
        return DataLoader(
            dataset,
            batch_size=self.hparams.batch_size,
            shuffle=False,
            num_workers=self.hparams.num_workers,
            pin_memory=True,
        )