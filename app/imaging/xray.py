"""Chest X-ray scores with TorchXRayVision (optional dependency).

Uses the DenseNet-121 "all" model and the preprocessing from the official
TorchXRayVision README: grayscale image normalised to [-1024, 1024], centre crop,
resize to 224x224. Outputs are model SCORES, not calibrated probabilities, and
are never shown as "% chance".
"""
from __future__ import annotations

import functools

import numpy as np

FLAG_THRESHOLD = 0.5  # design choice for the demo; studied in experiment E4


def available() -> bool:
    try:
        import torchxrayvision  # noqa: F401
        return True
    except Exception:
        return False


@functools.lru_cache(maxsize=1)
def _model():
    import torch
    import torchxrayvision as xrv
    torch.set_num_threads(max(1, torch.get_num_threads()))
    m = xrv.models.DenseNet(weights="densenet121-res224-all")
    m.eval()
    return m


def preprocess(img: np.ndarray) -> np.ndarray:
    """img: 2-D uint8 grayscale (or HxWx3) array -> 1x224x224 float32."""
    import torchvision
    import torchxrayvision as xrv
    if img.ndim == 3:
        img = img.mean(axis=2)
    x = xrv.datasets.normalize(img.astype(np.float32), 255)
    x = x[None, ...]
    tf = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),
                                         xrv.datasets.XRayResizer(224)])
    return tf(x)


def scores(img: np.ndarray) -> dict[str, float]:
    import torch
    m = _model()
    x = torch.from_numpy(preprocess(img))[None, ...]
    with torch.no_grad():
        out = m(x)[0].numpy()
    return {name: float(s) for name, s in zip(m.pathologies, out) if name}


def flagged(sc: dict[str, float], threshold: float = FLAG_THRESHOLD) -> tuple[list[str], list[str]]:
    yes = sorted(k for k, s in sc.items() if s >= threshold)
    no = sorted(k for k, s in sc.items() if s < threshold)
    return yes, no
