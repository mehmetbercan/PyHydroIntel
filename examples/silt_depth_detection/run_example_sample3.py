import sys
import os
import yaml

# Add parent directory to path to import from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.silt_detection import SiltDetector

def load_config(yaml_path):
    with open(yaml_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    # Load Config
    config_path = os.path.join(os.path.dirname(__file__), 'config_sample3.yaml')
    cfg = load_config(config_path)

    # Parse Config
    depths = cfg['observations']['depths']
    velocities = cfg['observations']['velocities']
    diameter = cfg['site_info']['diameter_m']
    slope = cfg['site_info']['slope']
    model_path = cfg['settings']['model_path']
    out_dir = cfg['settings']['output_dir']

    # Initialize Tool
    detector = SiltDetector(model_path=model_path)
    
    print(f"Generating plot for {diameter}m pipe...")
    img_path = detector.generate_plot(depths, velocities, diameter, slope, out_dir)
    
    print("Running AI analysis...")
    silt_m, silt_pct = detector.predict(img_path, diameter)
    
    print("-" * 30)
    print(f"Predicted Silt Height: {silt_m:.3f} m")
    print(f"Blockage Percentage:   {silt_pct * 100:.1f}%")
    print("-" * 30)

if __name__ == "__main__":
    main()

