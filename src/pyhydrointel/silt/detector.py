from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import tensorflow as tf
from PIL import Image


@dataclass
class SiltDetector:
    model_path: Path
    _model: Optional[tf.keras.Model] = None

    def __post_init__(self) -> None:
        self.model_path = Path(self.model_path)
        self.silt_ratios = [round(0.05 * i, 2) for i in range(13)]  # 0..60% step 5%

    def load_model(self) -> None:
        if self._model is None:
            self._model = tf.keras.models.load_model(self.model_path, compile=False)

    def predict_from_image(self, image_path: Path, diameter_m: float) -> Tuple[float, float]:
        self.load_model()

        img = Image.open(image_path)
        arr = np.asarray(img)[:, :, 0:3].astype(np.float32)  # drop alpha
        arr = np.expand_dims(arr, axis=0)
        arr[0] /= 255.0

        pred = self._model.predict(arr, verbose=0)
        idx = int(pred[0].argmax())

        ratio = self.silt_ratios[idx]
        height_m = ratio * float(diameter_m)
        return height_m, ratio