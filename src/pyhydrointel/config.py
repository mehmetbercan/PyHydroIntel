from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml


@dataclass
class SiteInfo:
    diameter_m: float
    slope: float


@dataclass
class Observations:
    depths: List[float]
    velocities: List[float]


@dataclass
class Settings:
    model_path: Path
    output_dir: Path


@dataclass
class SiltConfig:
    site_info: SiteInfo
    observations: Observations
    settings: Settings


def load_silt_config(path: Path) -> SiltConfig:
    path = Path(path)
    base = path.parent
    data = yaml.safe_load(path.read_text())

    site = data["site_info"]
    obs = data["observations"]
    sett = data["settings"]

    model_path = Path(sett["model_path"])
    output_dir = Path(sett["output_dir"])

    if not model_path.is_absolute():
        model_path = (base / model_path).resolve()
    if not output_dir.is_absolute():
        output_dir = (base / output_dir).resolve()

    cfg = SiltConfig(
        site_info=SiteInfo(float(site["diameter_m"]), float(site["slope"])),
        observations=Observations(
            [float(x) for x in obs["depths"]],
            [float(x) for x in obs["velocities"]],
        ),
        settings=Settings(model_path, output_dir),
    )

    if len(cfg.observations.depths) != len(cfg.observations.velocities):
        raise ValueError("observations.depths and observations.velocities must have same length")

    return cfg