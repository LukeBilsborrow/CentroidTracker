from typing import Union
import math
from PIL import Image

from typing import List


def pad_image_to_size(image: Union[List, Image.Image], target_size):
    if isinstance(image, list):
        image = Image.fromarray(image)

    target_w, target_h = target_size
    w, h = image.size

    if w > target_w or h > target_h:
        raise ValueError("Target dimensions cannot be larger than image current dimensions")

    padding = Image.new("RGB", target_size)
    padding.paste(image, (math.ceil((target_w-w)/2), math.ceil((target_h-h)/2)))
    return padding

if __name__ == "__main__":
    image_path = "C:/Users/lukex/Downloads/pepe.png"
    image = Image.open(image_path)
    size = [math.ceil(x*1.2) for x in image.size]
    print(size)
    pad_image_to_size(image, size)