from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO

CAPTION_HEIGHT = 100
TEXT_BUFFER = 20

# Extracts a PIL Image type from a direct link to the image
def extract_image_from_link(image_link):
    response = requests.get(image_link)
    img = Image.open(BytesIO(response.content))
    return img

# Add caption with species name, scientific name, photographer, etc to PIL Image
def add_caption(img, species_name, scientific_name, photographer_name):
    original_width, original_height = img.size
    new_width = original_width
    new_height = original_height + CAPTION_HEIGHT

    # Make new image with original dimensions but more height to allow for caption at bottom
    new_img = Image.new(mode = "RGB", size = (new_width, new_height), color = (60, 60, 60))

    # Paste original image onto new image
    offset = (0, 0)
    new_img.paste(img, offset)

    # Draw species name
    draw_species = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial_bold.ttf", 42)
    draw_species.text((TEXT_BUFFER, new_height - CAPTION_HEIGHT*0.75), species_name, (181, 200, 210), font=font)

    # Measure species name text width
    species_name_width = draw_species.textlength(species_name, font=font)

    # Draw scientific name
    draw_scientific = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial_italic.ttf", 42)
    draw_scientific.text((3*TEXT_BUFFER + species_name_width, new_height - CAPTION_HEIGHT*0.75), scientific_name, (255, 255, 255), font=font)

    # Measure scientific name text width
    scientific_name_width = draw_scientific.textlength(scientific_name, font=font)

    # Draw photographer name
    draw_photographer = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial_bold.ttf", 42)
    draw_photographer.text((5*TEXT_BUFFER + species_name_width + scientific_name_width, new_height - CAPTION_HEIGHT*0.75), f"© {photographer_name}", (255, 255, 255), font=font)

    # Measure photographer name text width
    photographer_name_width = draw_photographer.textlength(f"© {photographer_name}", font=font)

    # Draw Macaulay Library
    draw_library = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial.ttf", 42)
    draw_library.text((7*TEXT_BUFFER + species_name_width + scientific_name_width + photographer_name_width, new_height - CAPTION_HEIGHT*0.75), "Macaulay Library", (157, 157, 157), font=font)

    # Measure Macaulay Library text width
    library_width = draw_library.textlength("Macaulay Library", font=font)

    # Draw eBird
    draw_ebird = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial.ttf", 42)
    draw_ebird.text((9*TEXT_BUFFER + species_name_width + scientific_name_width + photographer_name_width + library_width, new_height - CAPTION_HEIGHT*0.75), "eBird", (157, 157, 157), font=font)

    return new_img