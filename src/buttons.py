import reddit as jp
import subprocess
from pathlib import Path
import shutil
import os

def download(save_path):
    path = str(Path(__file__).parent.parent / "response" / "response.jpg")
    
    try:
        shutil.copy(str(path), save_path)
        print(f"File successfully saved to: {save_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
    
    
    
def wallpaper():
    imagepath = str(Path(__file__).parent.parent / "response" / "response.jpg")
    scriptpath = str(Path(__file__).parent / "set_wallpaper")
    destinationpath = os.path.join(os.path.expanduser("~"), '.config', 'wallpaper')
    imagedestinationpath = f"{destinationpath}/wallpaper.jpg"
    
    try:
        if not os.path.isdir(destinationpath):
            print(f"Destination directory does not exist. Creating: {destinationpath}")
            os.makedirs(destinationpath)
        
        
        shutil.copy(imagepath, imagedestinationpath)
    
    except Exception as e:
        print(f"An error occurred: {e}")

    subprocess.run(["/bin/bash", scriptpath, imagedestinationpath])