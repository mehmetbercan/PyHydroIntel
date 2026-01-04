from __future__ import annotations

import argparse
import json
from pathlib import Path

from pyhydrointel.config import load_silt_config
from pyhydrointel.silt.detector import SiltDetector
from pyhydrointel.silt.plotter import generate_cnn_plot


def main() -> None:
    p = argparse.ArgumentParser(
        prog="pyhydrointel",
        description="Advanced AI & Hydroinformatics Tools for Wastewater Collection Systems.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    silt = sub.add_parser("silt-detect", help="Estimate silt height from depth/velocity series.")
    silt.add_argument("-c", "--config", required=True, type=Path, help="Path to YAML config.")
    silt.add_argument("--json", action="store_true", help="Print JSON output.")

    args = p.parse_args()

    if args.cmd == "silt-detect":
        cfg = load_silt_config(args.config)

        img_path = generate_cnn_plot(
            depths_m=cfg.observations.depths,
            velocities_ms=cfg.observations.velocities,
            diameter_m=cfg.site_info.diameter_m,
            slope=cfg.site_info.slope,
            output_dir=cfg.settings.output_dir,
        )

        det = SiltDetector(cfg.settings.model_path)
        height_m, ratio = det.predict_from_image(img_path, cfg.site_info.diameter_m)

        out = {"image_path": str(img_path), "silt_ratio": ratio, "silt_height_m": height_m}

        if args.json:
            print(json.dumps(out, indent=2))
        else:
            print(f"Image: {img_path}")
            print(f"Silt ratio: {ratio:.2f}")
            print(f"Silt height (m): {height_m:.6f}")