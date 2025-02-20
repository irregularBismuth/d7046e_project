import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Define the folder containing .NC files
folder_path = "Dataset\April"
output_folder = "processed_images"
os.makedirs(output_folder, exist_ok=True)

# List all .NC files in the directory
nc_files = [f for f in os.listdir(folder_path) if f.endswith(".nc")]

print(f"Found {len(nc_files)} NetCDF files in the folder.")

# Loop through each .NC file
for nc_file in nc_files:
    file_path = os.path.join(folder_path, nc_file)
    
    # Load the NetCDF file
    dataset = xr.open_dataset(file_path)
    
    # Extract first variable (assuming cloud mask)
    var_name = list(dataset.variables)[0]  # Adjust if needed
    cloud_mask = dataset[var_name].values  
    
    # Select first time step (if applicable)
    if cloud_mask.ndim == 3:
        cloud_mask = cloud_mask[0]  

    # Normalize cloud mask
    cloud_mask = (cloud_mask - np.min(cloud_mask)) / (np.max(cloud_mask) - np.min(cloud_mask))

    # Replace NaN values with 0
    cloud_mask = np.nan_to_num(cloud_mask)

    # Save cloud mask as a NumPy array
    output_path = os.path.join(output_folder, nc_file.replace(".nc", ".npy"))
    np.save(output_path, cloud_mask)

    # Save cloud mask as an image
    plt.imsave(output_path.replace(".npy", ".png"), cloud_mask, cmap="gray")

    print(f"Processed and saved: {output_path}")

print("All files processed successfully!")


