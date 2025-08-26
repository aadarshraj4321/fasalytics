# run_visualizer.py

import pyvista as pv
import numpy as np
import argparse
import sys
import os

# This script is designed to be called from the command line.

def generate_single_frame(output_path, moisture, width=100, length=150):
    """
    Generates a single 3D farm image frame and saves it to a file.
    This function is optimized for headless/server execution.
    """
    try:
        # Set the plot theme.
        pv.set_plot_theme("document")

        # Explicitly create the Plotter with off_screen=True.
        plotter = pv.Plotter(off_screen=True, window_size=[800, 600])

        # --- THE FIX IS HERE ---
        # Create the mesh points with the correct float data type from the start.
        # This will resolve the UserWarning.
        x = np.arange(0, width, 10, dtype=np.float32)
        y = np.arange(0, length, 10, dtype=np.float32)
        x, y = np.meshgrid(x, y)
        z = np.zeros_like(x, dtype=np.float32)
        # -------------------------

        farm_mesh = pv.StructuredGrid(x, y, z)

        # Add the soil moisture data to the mesh for coloring.
        farm_mesh["soil_moisture"] = np.full(farm_mesh.n_points, moisture)

        # Add the mesh to the plotter.
        # The invalid "force_float" argument has been removed.
        plotter.add_mesh(
            farm_mesh,
            scalars="soil_moisture",
            cmap="YlGnBu",
            scalar_bar_args={'title': "Soil Moisture"},
            clim=[0.0, 1.0]
        )
        
        # Add a text label.
        plotter.add_text(
            f"Average Soil Moisture: {moisture:.2f}",
            position="upper_edge",
            font_size=12,
            color="white"
        )

        # Set up a camera angle.
        plotter.camera_position = 'xy'
        plotter.camera.elevation = 45
        plotter.camera.zoom(1.2)
        plotter.enable_lightkit()

        # Ensure the output directory exists.
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Save the rendered scene.
        plotter.screenshot(output_path, return_img=False)

        # Close the plotter to free up resources.
        plotter.close()

    except Exception as e:
        # If there's an error, print it to stderr so the main process can see it.
        print(f"Error in visualizer script: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # This part of the script runs when it's called from the command line.
    parser = argparse.ArgumentParser(description="Generate a single 3D farm frame.")
    parser.add_argument("--output", required=True, help="Path to save the output PNG image.")
    parser.add_argument("--moisture", required=True, type=float, help="Soil moisture value (0.0 to 1.0).")
    
    args = parser.parse_args()

    # Call the main function with the provided arguments.
    generate_single_frame(output_path=args.output, moisture=args.moisture)