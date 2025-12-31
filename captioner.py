import urllib.request
from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO

import web_extraction
import image_editor

DIRECTORY_NAME = "renamed" # Name of local directory to save to in caption_txt_of_images

# Caption an image from Macaulay Library URL
def caption_image(link):
    # Extract image and data from URL
    [html, image_id] = web_extraction.extract_html_from_link(link)
    image_link = web_extraction.get_image_link_from_html(html, image_id)
    [species_name, scientific_name, photographer_name] = web_extraction.get_data_from_html(html)

    # Process image and add caption
    original_img = image_editor.extract_image_from_link(image_link)
    captioned_img = image_editor.add_caption(original_img, species_name, scientific_name, photographer_name)

    return captioned_img

# Caption every image in a txt of links and save to a directory
def caption_txt_of_images(textfile):
    # tba
    return


test_img = caption_image("https://macaulaylibrary.org/asset/204972611")
test_img.show()