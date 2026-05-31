**Add Logo to Image**

A Python utility to seamlessly add a PNG logo to images with batch processing capabilities. Perfect for photographers, content creators, and event organizers who need to watermark or brand multiple images with consistent placement and sizing.

### Features
- ✨ Add PNG logos to images with automatic aspect ratio preservation
- 📸 Batch process entire folders of images
- 🎯 Customizable logo size (default 10% of image width) and padding
- 🔄 Support for multiple image formats (JPG, JPEG, PNG, BMP, GIF, TIFF)
- 💾 Optional destination folder or in-place processing
- ✅ Error handling with detailed logging
- 🛠️ Simple configuration for easy customization

### Usage
1. Configure the source folder, destination folder, and logo path
2. Set `SINGLE_IMAGE_PATH` for single images or leave `None` for batch processing
3. Adjust `logo_scale` and `padding` values as needed
4. Run the script

### Example
```python
# Batch process all images
SOURCE_FOLDER = "path/to/images"
DESTINATION_FOLDER = "path/to/output"
LOGO_PATH = "path/to/logo.png"
```

### Requirements
- Python 3.x
- Pillow (PIL)

---

You can also add a shorter one-liner if needed:

**"Add a PNG logo to photos with batch processing support. Customize size, padding, and placement with ease."**
