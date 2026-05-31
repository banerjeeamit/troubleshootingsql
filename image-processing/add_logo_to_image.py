"""
Script to add a PNG logo to the bottom right corner of images.
The logo is scaled to 10% of the image width and positioned with 10 pixels padding.
Supports batch processing of multiple images with optional destination folder.

Known limitations:
1. This script is not aware if the pic needs to be rotated vertically or horizontally and due to this the logo can be added at the bottom right which might look out of place post the rotation.  
"""

from PIL import Image
import os
from pathlib import Path

# Configuration - Update these paths
SOURCE_FOLDER = "<add path name here>"  # Folder containing images
DESTINATION_FOLDER = "<add path name here>"  # Destination folder for processed images
LOGO_PATH = "<add path name here>"  # Path to the PNG logo
SINGLE_IMAGE_PATH = None  # Set to process a single image, or leave None to process all images in SOURCE_FOLDER

# Supported image formats
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')


def add_logo_to_image(image_path, logo_path, destination_path=None, logo_scale=0.1, padding=10):
    """
    Add a logo to the bottom right corner of an image.
    
    Args:
        image_path (str): Path to the original image file
        logo_path (str): Path to the PNG logo file
        destination_path (str): Path where the image should be saved. If None, overwrites original
        logo_scale (float): Scale logo to this percentage of image width (default: 0.1 = 10%)
        padding (int): Padding from edges in pixels (default: 10)
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    # Check if files exist
    if not os.path.exists(image_path):
        print(f"✗ Error: Image file not found: {image_path}")
        return False
    if not os.path.exists(logo_path):
        print(f"✗ Error: Logo file not found: {logo_path}")
        return False
    
    try:
        # Open the original image and store its format
        original_image = Image.open(image_path)
        original_format = original_image.format
        original_image = original_image.convert("RGB")
        
        # Open logo
        logo = Image.open(logo_path).convert("RGBA")
        
        # Get dimensions
        img_width, img_height = original_image.size
        
        # Calculate new logo size (scale to percentage of image width)
        new_logo_width = int(img_width * logo_scale)
        aspect_ratio = logo.size[1] / logo.size[0]
        new_logo_height = int(new_logo_width * aspect_ratio)
        
        # Resize logo while maintaining aspect ratio
        logo = logo.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)
        
        # Calculate position (bottom right corner with padding)
        position_x = img_width - new_logo_width - padding
        position_y = img_height - new_logo_height - padding
        
        # Composite the logo onto the image
        original_image.paste(logo, (position_x, position_y), logo)
        
        # Determine save path
        save_path = destination_path if destination_path else image_path
        
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the image
        original_image.save(save_path)
        print(f"✓ Logo added successfully to: {save_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {image_path}: {e}")
        return False


def process_batch_images(source_folder, logo_path, destination_folder=None, logo_scale=0.1, padding=10):
    """
    Process all images in a folder and add logo to each.
    
    Args:
        source_folder (str): Folder containing image files
        logo_path (str): Path to the PNG logo file
        destination_folder (str): Folder where processed images will be saved. 
                                 If None, overwrites original files
        logo_scale (float): Scale logo to this percentage of image width
        padding (int): Padding from edges in pixels
    
    Returns:
        tuple: (successful_count, failed_count)
    """
    
    if not os.path.isdir(source_folder):
        print(f"✗ Error: Source folder not found: {source_folder}")
        return 0, 0
    
    if not os.path.exists(logo_path):
        print(f"✗ Error: Logo file not found: {logo_path}")
        return 0, 0
    
    # Get all image files
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(Path(source_folder).glob(f"*{ext}"))
        image_files.extend(Path(source_folder).glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"✗ No image files found in: {source_folder}")
        return 0, 0
    
    print(f"\nProcessing {len(image_files)} image(s) from: {source_folder}")
    print(f"Destination: {destination_folder if destination_folder else source_folder}")
    print("-" * 60)
    
    successful = 0
    failed = 0
    
    for image_path in sorted(image_files):
        # Determine destination path
        if destination_folder:
            save_path = os.path.join(destination_folder, image_path.name)
        else:
            save_path = None  # Will overwrite original
        
        if add_logo_to_image(str(image_path), logo_path, save_path, logo_scale, padding):
            successful += 1
        else:
            failed += 1
    
    print("-" * 60)
    print(f"\nBatch processing complete:")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")
    
    return successful, failed


if __name__ == "__main__":
    # Process single image or batch
    if SINGLE_IMAGE_PATH:
        # Process single image
        print(f"Processing single image: {SINGLE_IMAGE_PATH}")
        add_logo_to_image(SINGLE_IMAGE_PATH, LOGO_PATH)
    else:
        # Process all images in source folder
        process_batch_images(SOURCE_FOLDER, LOGO_PATH, DESTINATION_FOLDER)
