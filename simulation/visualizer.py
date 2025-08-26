# simulation/visualizer.py

import os
import sys

# Set environment variables BEFORE importing PyVista to ensure off-screen rendering.
# This is crucial for running in headless or server environments.
if 'pytest' not in sys.modules:
    os.environ['PYVISTA_OFF_SCREEN'] = 'true'
    os.environ['VTK_USE_OFFSCREEN'] = 'true'

import pyvista as pv
import numpy as np

# Set a theme that is friendly for headless environments.
pv.set_plot_theme("document")


def generate_3d_farm_image(
    width=100,
    length=150,
    soil_moisture=0.6,
    output_path="farm_visualization.png"
):
    """
    Generates a 3D image of a farm plot using a forced off-screen backend.
    """
    try:
        # The plotter will automatically be off-screen due to the environment variables.
        plotter = pv.Plotter()

        # Create the 3D mesh for the farm plot.
        x = np.arange(0, width, 10)
        y = np.arange(0, length, 10)
        x, y = np.meshgrid(x, y)
        z = np.zeros_like(x)
        farm_mesh = pv.StructuredGrid(x, y, z)

        # Add the soil moisture data to the mesh for coloring.
        farm_mesh["soil_moisture"] = np.full(farm_mesh.n_points, soil_moisture)

        # Add the mesh to the plotter.
        plotter.add_mesh(
            farm_mesh,
            scalars="soil_moisture",
            cmap="YlGnBu",
            scalar_bar_args={'title': "Soil Moisture"},
            clim=[0.0, 1.0]
        )
        
        # Add a text label for context.
        plotter.add_text(
            f"Average Soil Moisture: {soil_moisture:.2f}",
            position="upper_edge",
            font_size=12,
            color="white"
        )

        # Set up a good camera angle.
        plotter.camera_position = 'xy'
        plotter.camera.elevation = 45
        plotter.camera.zoom(1.2)
        plotter.enable_lightkit()

        # Ensure the output directory exists before saving.
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Save the rendered scene to the specified file.
        plotter.screenshot(output_path, return_img=False)

        # Close the plotter to free up system resources.
        plotter.close()
        
        # This print statement can be useful for logging when called from a subprocess.
        # print(f"Subprocess: Successfully generated 3D farm image at {output_path}")
        return True

    except Exception as e:
        print(f"Subprocess Error: An error occurred during 3D visualization: {e}")
        return False