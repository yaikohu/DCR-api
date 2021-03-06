import numpy as np
from sklearn.cluster import KMeans
import requests
from PIL import Image

import io


def rgb_to_hex(rgb: tuple) -> str:
    """
    Accepts a tuple of RGB values (R: int, G: int, B: int)
    Turns the rgb values to a hexadecimal value.
    Returns the hexadecimal value as a string.
    """

    return '%02x%02x%02x' % rgb


def read_img(f) -> np.asarray:
    """
    Reads a file and returns a np.asarray.
    input: image file
    output: np.asarray
    """
    with Image.open(f) as img:
        img.convert("RGB")
        img.thumbnail((300, 300))
    return np.asarray(img)


def fetch_and_read_image(url: str) -> np.asarray:
    """
    Required for extracting an image from a request object.

    input: url string
    output: np.asarray containing the rgb values of every pixel of the image.
    """
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        try:
            pil_img = Image.open(io.BytesIO(response.content)).convert("RGB")
            pil_img.thumbnail((200, 200))
            img = np.asarray(pil_img)
            return img
        except:
            print('Could not load the image from the provided URL.')
    else:
        return f"Couldn't retrieve the image. Status code: {response.status_code}"


def get_dominant_colors(url: str, N_CLUSTERS=3) -> list:
    """
    Accepts an url (str) to an image.
    Retrieves the dominant colors through clustering.
    Returns the amount N_CLUSTERS colors within an array.
    """

    # Fetches image from url and saves it as a cv2 image object
    IMAGE = fetch_and_read_image(url)

    height, width, channels = IMAGE.shape

    #  Checks if the image has color values
    try:
        assert channels == 3
        # Reshaping the image array for the KMeans algorithm

        IMAGE = IMAGE.reshape((height * width), channels)

        # Clustering the image
        IMG_CLUSTER = KMeans(n_clusters=N_CLUSTERS).fit(IMAGE)

        # Contains the dominant colors of the image
        CLUSTER_CENTERS = IMG_CLUSTER.cluster_centers_

        # An empty list in which the color values will be put into.
        rgb_hex_values = []

        for i in range(N_CLUSTERS):
            # Determines the RGB value of every cluster
            RGB = (round(CLUSTER_CENTERS[i][0]), round(
                CLUSTER_CENTERS[i][1]), round(CLUSTER_CENTERS[i][2]))

            # Appends the RGB-turned Hex values to the rgb_hex_values list
            rgb_hex_values.append((rgb_to_hex(RGB)))

        colors = []
        for color in rgb_hex_values:
            if color not in colors:
                colors.append(color)
        colors.sort()

        return colors

    except AssertionError as msg:
        return f"The image does not have any color values."
