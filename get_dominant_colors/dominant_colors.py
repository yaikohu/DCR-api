import json
import numpy as np
import cv2
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import requests
from PIL import Image
import io

# TODO: Split the code into respective functions.

# IDEA: Create a class?

DB = "../data/db_full_logo_urls.json"
data = json.load(open(DB))

N_CLUSTERS: int = 3
RGB_VALUES = []

def convert_from_pil_to_cv2(img: Image) -> np.asarray:
    return np.asarray(img)


def fetch_and_save_image(url: str) -> np.asarray:
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)

    PIL_IMG = Image.open(image_bytes)
    IMG = convert_from_pil_to_cv2(PIL_IMG)

    return IMG 



# Info src1: https://stackoverflow.com/a/14678150
# Info src2: https://stackoverflow.com/a/3380754
# Used: src3: https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/

def rgb_to_hex(rgb: tuple) -> str:
    return '%02x%02x%02x' % rgb


def get_dominant_color(company_data_json, company_name: str) -> list:
    logo_url = company_data_json[company_name]['logo']
    IMAGE = fetch_and_save_image(logo_url)

    height, width, channels = IMAGE.shape
    assert channels == 3
    IMAGE = IMAGE.reshape((height * width), channels)

    IMG_CLUSTER = KMeans(n_clusters = N_CLUSTERS).fit(IMAGE)
    CLUSTER_CENTERS = IMG_CLUSTER.cluster_centers_

    rgb_hex_values = []

    for i in range(N_CLUSTERS):
        RGB = (round(CLUSTER_CENTERS[i][0]), round(CLUSTER_CENTERS[i][1]), round(CLUSTER_CENTERS[i][2]))

        rgb_hex_values.append((rgb_to_hex(RGB)))
    
    return rgb_hex_values

# print(get_dominant_color(data, "Rabobank"))
# print(" \n")

# Looping over every company logo
for key in data:
    if key == "Rabobank":
        logo_url = data[key]['logo']

        response = requests.get(logo_url)
        image_bytes = io.BytesIO(response.content)

        PIL_IMG = Image.open(image_bytes)
        PIL_IMG_PIXELS = PIL_IMG.load()
        
        for i in range(PIL_IMG.size[0]): # for every pixel:
            for j in range(PIL_IMG.size[1]):
                if PIL_IMG_PIXELS[i,j] == (255, 255, 255): # if not black:
                    PIL_IMG_PIXELS[i,j] = (255, 255, 255) # change to white



        # # Converting PIL_IMG to opencv image
        # IMAGE = convert_from_pil_to_cv2(PIL_IMG)

        # # Unpacking the dimensions of the image into variables
        # height, width, channels = IMAGE.shape
        
        # # Checks if the image has color channels
        # assert channels == 3

        # # Reshapes the image ndarray to a 2d array with the rgb values on each row
        # IMAGE = IMAGE.reshape((height * width), channels)

        # print(IMAGE)


        # # Clustering the 2d-nparray
        # IMG_CLUSTER = KMeans(n_clusters = N_CLUSTERS).fit(IMAGE)

        # # The dominant colours are the center clusters
        # CLUSTER_CENTERS = IMG_CLUSTER.cluster_centers_

        # # Iterating over the clusters and returning the RGB values in HEX
        # for i in range(0, N_CLUSTERS):
        #     # Splitting the RGB values from the clusters and putting them in a tuple: RGB
        #     RGB = (r, g, b) = (round(CLUSTER_CENTERS[i][0]), round(CLUSTER_CENTERS[i][1]), round(CLUSTER_CENTERS[i][2]))
            
        #     # Converting RGB to hex values
        #     print(rgb_to_hex(RGB))
