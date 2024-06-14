import os
import requests
from tqdm import tqdm

def create_directory(path):
    """Create directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created: {path}")
    else:
        print(f"Directory already exists: {path}")

def download_file(url, folder_path, file_name=None):
    """Download a file from a given URL to a specified folder with an optional file name."""
    local_filename = file_name if file_name else url.split('/')[-1]
    local_filepath = os.path.join(folder_path, local_filename)

    # Stream download to handle large files
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024 # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(local_filepath, 'wb') as f:
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
    else:
        print(f"Downloaded {local_filename} to {folder_path}")

# Define the folders and their corresponding file URLs with optional file names
folders_and_files = {
    os.path.join("SUPIR", "models", "checkpoints"): [
        ("https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors", None),
        ("https://civitai.com/api/download/models/360292?token=22c5b4cb1989d2c3ff29f222d2840884", "WildCardX_XL_Lightning.safetensors")
    ]
}


# Perform the download process
for folder, files in folders_and_files.items():
    create_directory(folder)
    for file_url, file_name in files:
        download_file(file_url, folder, file_name)
