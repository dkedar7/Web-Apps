import os
import math
import numpy as np
import requests
import tempfile
import base64
from io import BytesIO
from dotenv import load_dotenv

from fast_dash import FastDash, UploadImage, PIL, Image
from PIL import ImageOps, ImageEnhance
from fast_dash.utils import _pil_to_b64, _b64_to_pil

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/thiagohersan/maskformer-satellite-trees"
headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


# Build and deploy!
# If running locally, feel free to drop the mode and port arguments.
def detect_vegetation_from_satellite_images(upload_image: UploadImage, or_select_an_example: str = ["Manhattan", "Oakland", "Cesario", "Artshack"]) -> (Image, Image, str):
    """
    Upload a satellite image and let this image segmentation model detect vegetation.\
    The model is a MaskFormer trained on a very small number (25) of manually labeled images.\
    As a result, although the model is not very accurate, it can be used to quickly detect vegetation in satellite images.\
    Click 'About' to learn more about.
    
    Learn more about the model and training [here](https://huggingface.co/thiagohersan/maskformer-satellite-trees).

    :param upload_image: An image uploaded by the user.
    :type upload_image: PIL.Image

    :return original_image : PIL.Image
    :rtype original_image: PIL.Image

    :return result_masked_image: The original image with a green overlay on vegetation and a red overlay on non-vegetation.
    :rtype result_masked_image: PIL.Image

    :return vegetation_percentage: The percentage of vegetation in the image.
    :rtype vegetation_percentage: str
    """
    
    if upload_image is None:
        print (os.getcwd())
        upload_image = PIL.Image.open(os.path.join(os.getcwd(), "examples", f"{or_select_an_example}.jpg"))
        file_extension = ".jpg"
        
    else:
        # Determine the format of the uploaded PIL image
        format = upload_image.format
        file_extension = ".jpg" if format == "JPEG" else ".png"

    with tempfile.NamedTemporaryFile(delete=True) as f:
        upload_image.save(f.name + file_extension)

        response_images = query(f.name + file_extension)
        vegetation_image_mask = [r for r in response_images if r["label"] == "vegetation"]

        if len(vegetation_image_mask) == 0:
            result_image = PIL.Image.new("RGBA", upload_image.size, (0, 0, 0, 0))

        else:
            result_image = base64.b64decode(vegetation_image_mask[0]['mask'])
            result_image = PIL.Image.open(BytesIO(result_image))

    original_image = upload_image

    # Convert original image to RGBA
    original_image_rgba = original_image.convert("RGBA")

    # Create a colored mask for vegetation
    green_mask = PIL.Image.new("RGBA", result_image.size, (0, 255, 0, 100))  # Green with alpha 0.7
    red_mask = PIL.Image.new("RGBA", result_image.size, (255, 0, 0, 100))  # Red with alpha 0.7

    # Convert the result image to a mask
    result_mask = result_image.convert("L")
    result_mask = ImageEnhance.Contrast(result_mask).enhance(2.0)  # Enhance mask contrast if needed
    result_mask = result_mask.point(lambda x: 0 if x < 128 else 255)  # Binary threshold

    # Convert binary mask to RGBA
    result_mask_rgba = PIL.Image.new("RGBA", result_mask.size)
    result_mask_rgba.putalpha(result_mask)

    # Apply the green mask to the vegetation areas
    vegetation_overlay = PIL.Image.composite(green_mask, original_image_rgba, result_mask_rgba)

    # Invert the mask for non-vegetation areas
    non_vegetation_mask = ImageOps.invert(result_mask)
    non_vegetation_mask_rgba = PIL.Image.new("RGBA", non_vegetation_mask.size)
    non_vegetation_mask_rgba.putalpha(non_vegetation_mask)

    # Apply the red mask to the non-vegetation areas
    final_overlay = PIL.Image.composite(red_mask, vegetation_overlay, non_vegetation_mask_rgba)

    # Blend the overlay with the original image
    result_masked_image = PIL.Image.alpha_composite(original_image_rgba, final_overlay)

    # Convert the result image to a binary mask (non-zero for vegetation areas)
    binary_vegetation_mask = result_mask.point(lambda x: 255 if x >= 128 else 0)

    # Calculate the number of non-zero (vegetation) pixels
    non_zero_pixels = np.count_nonzero(np.array(binary_vegetation_mask))

    # Calculate the total number of pixels
    total_pixels = binary_vegetation_mask.size[0] * binary_vegetation_mask.size[1]

    # Calculate the percentage of vegetation
    vegetation_percentage = (non_zero_pixels / total_pixels) * 100
    vegetation_percentage =f"Approximately {math.floor(vegetation_percentage)}% of this scene is vegetation."

    return original_image, result_masked_image, vegetation_percentage

# Output mosaic
output_mosaic = """
AB
AB
AB
CC
"""

app = FastDash(detect_vegetation_from_satellite_images, theme="Yeti", mosaic=output_mosaic)
server = app.server

if __name__ == "__main__":
    app.run()