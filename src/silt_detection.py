import os
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
from matplotlib import pyplot as plt

class SiltDetector:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        # Silt depths as % of pipe diameter (0% to 60%)
        self.silt_ratios = [round(float("%.2f" % (0.05 * i)), 2) for i in range(0, 13)]

    def load_model(self):
        if not self.model:
            self.model = tf.keras.models.load_model(self.model_path, compile=False)

    def generate_plot(self, depths, velocities, diameter, slope, output_dir):
        """Generates the specific scatter plot required by the CNN."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        csz = diameter
        df = pd.DataFrame({'Depth': depths, 'Velocity': velocities})
        
        # Determine Wet vs Dry logic based on max depth
        is_wet = max(depths) >= csz
        weather_type = 'wet' if is_wet else 'dry'
        
        # Plot limits
        if is_wet:
            y_lim = [-0.1, 5]
            x_lim = [-6, 8]
        else:
            y_lim = [-0.1, 3]
            x_lim = [-3, 5]

        # Plotting
        fig = plt.figure(num=1, clear=True, figsize=(2, 2))
        ax = fig.add_subplot()
        
        df.plot.scatter(x='Velocity', y='Depth', s=10, c='#026a9e', alpha=1, ax=ax)
        
        # Draw Reference Lines (Conduit, Slope, etc)
        ax.plot(x_lim, [csz, csz], zorder=-1, color='#595959', linewidth=0.8) # Top
        # (Add other slope lines here as per original code if needed for visual debugging)

        ax.set_ylim(y_lim)
        ax.set_xlim(x_lim)
        
        # Clean specific formatting for CNN input
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        if ax.get_legend(): ax.get_legend().remove()
        plt.grid()

        filename = f"{weather_type}_csz{diameter:.2f}_slope{slope}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, bbox_inches='tight')
        plt.close(fig)
        
        return filepath

    def predict(self, image_path, diameter):
        self.load_model()
        
        # Preprocess
        img = Image.open(image_path)
        img_arr = np.asarray(img)[:, :, 0:3] # Remove alpha
        img_arr = np.array([img_arr]).astype(np.float32)
        img_arr[0] = img_arr[0] / 255.0 # Normalize

        # Inference
        prediction = self.model.predict(img_arr, verbose=0)
        idx = prediction[0].argmax()
        
        silt_ratio = self.silt_ratios[idx]
        silt_height_m = silt_ratio * diameter
        
        return silt_height_m, silt_ratio