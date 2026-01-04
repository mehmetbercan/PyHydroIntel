from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pandas as pd
from PIL import Image

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def generate_cnn_plot(
    depths_m: Sequence[float],
    velocities_ms: Sequence[float],
    diameter_m: float,
    slope: float,
    output_dir: Path,
) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.rcParams["figure.dpi"] = 72.0
    plt.rcParams["savefig.dpi"] = "figure"
    plt.rcParams["savefig.pad_inches"] = 0.1
    plt.rcParams["font.size"] = 10.0

    csz = float(diameter_m)
    df = pd.DataFrame({"Depth": depths_m, "Velocity": velocities_ms})

    is_wet = max(depths_m) >= csz
    weather = "wet" if is_wet else "dry"

    if is_wet:
        y_lim = [-0.1, 5]
        x_lim = [-6, 8]
    else:
        y_lim = [-0.1, 3]
        x_lim = [-3, 5]

    fig = plt.figure(num=1, clear=True, figsize=(2, 2), dpi=72.0)
    ax = fig.add_subplot()

    df.plot.scatter(x="Velocity", y="Depth", s=10, c="#026a9e", alpha=1, ax=ax)
    ax.plot(x_lim, [csz, csz], zorder=-1, color="#595959", linewidth=0.8)

    ax.set_ylim(y_lim)
    ax.set_xlim(x_lim)

    for sp in ("top", "right", "bottom", "left"):
        ax.spines[sp].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    if ax.get_legend():
        ax.get_legend().remove()
    plt.grid()

    filename = f"{weather}_csz{diameter_m:.2f}_slope{slope}.png"
    path = output_dir / filename

    plt.savefig(path, bbox_inches="tight", dpi=72.0, pad_inches=0.1)
    plt.close(fig)

    # CNN expects (W=126, H=123)
    with Image.open(path) as im:
        if im.size != (126, 123):
            im = im.resize((126, 123), Image.LANCZOS)
            im.save(path)

    return path