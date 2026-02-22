import os
import subprocess
import urllib.request
import zipfile
import sys

# -------------------------------------------------------------
# FFmpeg Installer (Windows)
# Downloads the official FFmpeg release, extracts it, moves
# executables to C:\ffmpeg\bin, and adds it to the system PATH.
# Robust error handling included.
# -------------------------------------------------------------

try:
    # Installation directory
    install_dir = 'C:\\ffmpeg'
    bin_dir = os.path.join(install_dir, 'bin')
    os.makedirs(bin_dir, exist_ok=True)

    # URL for official FFmpeg Windows static build
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    # Path to save the ZIP file
    zip_path = os.path.join(install_dir, "ffmpeg.zip")

    # Download FFmpeg ZIP
    if not os.path.exists(zip_path):
        print("Downloading FFmpeg...")
        try:
            urllib.request.urlretrieve(ffmpeg_url, zip_path)
            print("Download complete.")
        except Exception as e:
            print(f"Error during download: {e}")
            sys.exit(1)

    # Extract the ZIP file
    print("Extracting FFmpeg...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(install_dir)
        print("Extraction complete.")
    except zipfile.BadZipFile as e:
        print(f"Extraction failed (bad ZIP file): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Extraction failed: {e}")
        sys.exit(1)

    # Locate the extracted folder (usually versioned)
    subfolders = [f.path for f in os.scandir(install_dir) if f.is_dir() and "ffmpeg" in f.name.lower()]
    if not subfolders:
        print("Error: FFmpeg folder not found after extraction.")
        sys.exit(1)
    extracted_folder = subfolders[0]

    # Move ffmpeg.exe and ffprobe.exe to bin_dir
    for exe_name in ["ffmpeg.exe", "ffprobe.exe"]:
        try:
            src = os.path.join(extracted_folder, "bin", exe_name)
            dst = os.path.join(bin_dir, exe_name)
            if os.path.exists(src):
                os.replace(src, dst)
        except Exception as e:
            print(f"Error moving {exe_name}: {e}")
            sys.exit(1)

    # Clean up temporary files
    try:
        os.remove(zip_path)
        # Remove leftover extracted folder
        for root, dirs, files in os.walk(extracted_folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(extracted_folder)
    except Exception as e:
        print(f"Warning: Cleanup failed: {e}")

    # Add FFmpeg to PATH if not already present
    current_path = os.environ.get("PATH", "")
    if bin_dir not in current_path:
        try:
            new_path = f"{bin_dir};{current_path}"
            subprocess.call(["setx", "PATH", new_path])
            print("FFmpeg has been added to the system PATH.")
        except Exception as e:
            print(f"Failed to update PATH: {e}")

    print("Installation completed successfully. You may close this installer.")

except Exception as e:
    # Catch any other unexpected errors
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)