import urllib.request
from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO
import os 
import sys

import web_extraction
import image_editor

DIRECTORY_NAME = "captioned" # Name of local directory to save to in caption_txt_of_images
TEMPORARY_TXT_NAME = "temp.txt" # Temporary txt name to use for multiple command line arguments, will be overwritten

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
# Format must be: One link on each line
def caption_txt_of_images(textfile):
    # If directory does not exist, make directory for all images to be saved in
    if not os.path.exists(DIRECTORY_NAME):
        os.mkdir(DIRECTORY_NAME)
    
    try: 
        with open(textfile) as file:
            lines = [line.rstrip() for line in file]
    except: 
        print("ERROR: Given .txt file does not exist")

    i = 0
    num_of_lines = len(lines)
    while i < num_of_lines:
        curr_line = lines[i]
        # Check if current line contains a valid Macaulay Library asset link
        if check_link(curr_line):
            curr_img = caption_image(curr_line)
            [curr_html, curr_image_id] = web_extraction.extract_html_from_link(curr_line)
            curr_img.save(f"{DIRECTORY_NAME}/{curr_image_id}.png", "PNG")
            
            if i+1 == num_of_lines:
                print(f"Link {i+1} out of {num_of_lines} processed into image.")
            else:
                print(f"Link {i+1} out of {num_of_lines} processed into image...")
        else: 
            print(f"Link {i} out of {num_of_lines} not a valid Macaulay Library asset link and has been skipped.")

        i+=1
    return

# Checks if a link is a valid Macaulay Library asset link, return False if it isn't
def check_link(link):
    if "https://macaulaylibrary.org/asset/" not in link:
        return False
    return True

def main():
    # If more than 1 command line argument, automatically treat as a list of links
    if len(sys.argv) > 2:
        # Convert into temporary txt file
        with open(TEMPORARY_TXT_NAME, "w") as f:
            i = 1 # Skip first cmd line argument
            # Write every valid command line argument into temporary txt file
            while i < len(sys.argv):
                curr_argument = sys.argv[i]
                f.write(f"{curr_argument}\n")
                i+=1
        f.close()

        # Caption each file in txt
        caption_txt_of_images(TEMPORARY_TXT_NAME)

        # Remove temporary txt file after captioning complete
        os.remove(TEMPORARY_TXT_NAME)

    elif len(sys.argv) == 2:
        # If one argument only, treat as single link OR txt file input
        arg = sys.argv[1]

        if arg.endswith("txt") or arg.endswith("TXT"):
            # Input is a txt file input
            caption_txt_of_images(arg)
        elif check_link(arg):
            # Input is a valid Macaulay Library asset link
            img = caption_image(arg)
            [html, image_id] = web_extraction.extract_html_from_link(arg)
            img.save(f"{image_id}.png", "PNG")
        else: 
            print("ERROR: Input is not a valid Macaulay Library asset link nor txt file.")

        



if __name__ == "__main__":
    main()