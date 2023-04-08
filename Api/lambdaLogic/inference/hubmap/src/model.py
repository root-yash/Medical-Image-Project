from torch import nn
import pytorch_lightning as pl
from lightning_module import FlexibleUNet
from config import BACKBONE
import monai
import torch 
from typing import Dict

class LitModule(pl.LightningModule):
    def __init__(
        self,
        model: str,
        loss: str,
        spatial_size: int,
        learning_rate: float,
        weight_decay: float,
    ):
        super().__init__()

        self.save_hyperparameters()

        self.model = self._init_model()

        self.loss_fn = self._init_loss_fn()

        # TODO: add metric

    def _init_model(self) -> nn.Module:
        spatial_size = (self.hparams.spatial_size, self.hparams.spatial_size)
        
        if self.hparams.model == "unet":
            return FlexibleUNet(
                in_channels=1,
                out_channels=1,
                backbone = BACKBONE,
                pretrained=False
            )
        elif self.hparams.model == "attention_unet":
            return monai.networks.nets.AttentionUnet(
                spatial_dims=2,
                in_channels=3,
                out_channels=1,
                channels=(16, 32, 64, 128, 256),
                strides=(2, 2, 2, 2),
            )
        elif self.hparams.model == "unetr":
            return monai.networks.nets.UNETR(
                in_channels=3,
                img_size=spatial_size,
                out_channels=1,
                spatial_dims=2,
            )
        elif self.hparams.model == "swin_unetr":
            return monai.networks.nets.SwinUNETR(
                img_size=spatial_size,
                in_channels=3,
                out_channels=1,
                spatial_dims=2,
            )

    def _init_loss_fn(self):
        if self.hparams.loss == "dice":
            return monai.losses.DiceLoss(sigmoid=True)
        elif self.hparams.loss == "bce":
            return nn.BCEWithLogitsLoss()

    def configure_optimizers(self):
        # TODO: try other optimizers and schedulers
        return torch.optim.Adam(
            params=self.parameters(), lr=self.hparams.learning_rate, weight_decay=self.hparams.weight_decay
        )

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        return self.model(images)

    def training_step(self, batch: Dict, batch_idx: int) -> torch.Tensor:
        images, masks = batch["image"], batch["mask"]
        outputs = self(images)

        loss = self.loss_fn(outputs, masks)

        self.log("train_loss", loss, batch_size=images.shape[0])

        return loss

    def validation_step(self, batch: Dict, batch_idx: int) -> None:
        images, masks = batch["image"], batch["mask"]
        outputs = self(images)

        loss = self.loss_fn(outputs, masks)

        self.log("val_loss", loss, prog_bar=True, batch_size=images.shape[0])

    @classmethod
    def load_eval_checkpoint(cls, checkpoint_path: str, device: str) -> nn.Module:
        module = cls.load_from_checkpoint(checkpoint_path=checkpoint_path).to(device)
        module.eval()

        return module