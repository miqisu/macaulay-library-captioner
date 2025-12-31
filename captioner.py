import urllib.request
from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO
import os 

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
# Format must be: One link on each line, no spaces
def caption_txt_of_images(textfile):
    # If directory does not exist, make directory for all images to be saved in
    if not os.path.exists(DIRECTORY_NAME):
        os.mkdir(DIRECTORY_NAME)
    
    with open(textfile) as file:
        lines = [line.rstrip() for line in file]

    i = 0
    num_of_lines = len(lines)
    while i < num_of_lines:
        curr_line = lines[i]
        curr_img = caption_image(curr_line)
        [curr_html, curr_image_id] = web_extraction.extract_html_from_link(curr_line)
        curr_img.save(f"{DIRECTORY_NAME}/{curr_image_id}.png", "PNG")
        
        if i+1 == num_of_lines:
            print(f"Link {i+1} out of {num_of_lines} processed into image.")
        else:
            print(f"Link {i+1} out of {num_of_lines} processed into image...")
        
        i+=1
    return


caption_txt_of_images("test.txt")
# test_img = caption_image("https://macaulaylibrary.org/asset/204972611")
# test_img.show()