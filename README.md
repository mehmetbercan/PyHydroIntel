# PyHydroIntel

**Advanced AI & Hydroinformatics Tools for Wastewater Collection Systems**

PyHydroIntel is a repository of Python-based tools designed to enhance the operation and maintenance of urban drainage systems. By leveraging Deep Learning and hydraulic modeling, this project aims to prevent Sanitary Sewer Overflows (SSOs) and Combined Sewer Overflows (CSOs).

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

