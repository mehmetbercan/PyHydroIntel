# PyHydroIntel

![License: Research-Only](https://img.shields.io/badge/license-Research--Only-orange)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Status](https://img.shields.io/badge/status-early--stage-lightgrey)

**Advanced AI & Hydroinformatics Tools for Wastewater Collection Systems**

PyHydroIntel is a repository of Python-based tools designed to enhance the operation and maintenance of urban drainage systems. By leveraging Deep Learning and hydraulic modeling, this project aims to prevent Sanitary Sewer Overflows (SSOs) and Combined Sewer Overflows (CSOs).

## Installation

If you’re new, please read [**Help for Novice Users.md**](Help%20for%20Novice%20Users.md) first.  
Then open a terminal in your project root (where `pyproject.toml` is).

1. **Clone the repository:**  
(Alternatively, download the ZIP file from the repository page and extract it)

```
git clone https://github.com/mehmetbercan/PyHydroIntel.git
cd PyHydroIntel
```

2. **Create a virtual environment + install (editable):**

```
python -m venv .venv
pip install -e .
```

*Note: Requires Python 3.9+.*

## Usage

The tool uses a YAML configuration file to manage input data (depths/velocities) and site parameters.

1. **Edit the example YAML config:**
- File: `examples/silt_config.yaml`
- Update:
  - `observations.depths` and `observations.velocities`
  - `site_info.diameter_m` and `site_info.slope`
  - (Optional) `settings.output_dir`

2. **Run silt detection from repo root:**

```
pyhydrointel silt-detect -c examples/silt_config.yaml
```

3. **JSON output (optional):**

```
pyhydrointel silt-detect -c examples/silt_config.yaml --json
```

**Note on paths:** `settings.model_path` and `settings.output_dir` are resolved **relative to the YAML file location**.

## Available Modules

### 1. Silt & Blockage Detection (CNN-Based)

*A Deep Convolutional Neural Network for identifying solid waste accumulation using depth-velocity relationships.*

**The Problem:**  
Solid waste accumulation leads to blockages and reduced capacity. Current automated methods often rely solely on depth data, missing the velocity information essential for accurate silt depth determination.

**Our Solution:**  
We trained a Deep CNN on depth-velocity scatter plots generated from over 1.4 million SWMM simulations. The model detects blockage levels without requiring manual parameter adjustments in Manning's equation.

**Key Performance Metrics:**
- **Accuracy:** 99% (for predictions with deviations up to 10%).
- **Training Data:** 82,482 labeled plots from SWMM simulations.
- **Validation:** Tested on physical experiments (20 cm pipes).
- **Precision:** Real-world predictions fell within 0 cm, 0.3 cm, and 1.5 cm of actual blockage depths.

## Citation

If you rely on this module for your research, please cite:

> Ercan, M. B. "Leveraging AI to Identify Silt Accumulation and Blockage in Collection Systems." *Uludağ Üniversitesi Mühendislik Fakültesi Dergisi*, (Advanced Online Publication), 997-1010.

## License

**Strictly for academic research, educational, or non-profit use only.**  
Commercial use, selling, or incorporating this into proprietary products is **strictly prohibited** without written permission. See `LICENSE` file for details.