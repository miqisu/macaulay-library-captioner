from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO

# Extracts a PIL Image type from a direct link to the image
def extract_image_from_link(image_link):
    response = requests.get(image_link)
    img = Image.open(BytesIO(response.content))
    return img

# Add caption with species name, scientific name, photographer, etc to PIL Image
def add_caption(img, species_name, scientific_name, photographer_name, caption_height, text_buffer, font_size):
    original_width, original_height = img.size

    # Calculate caption height, text buffer and font size depending on size of image
    if caption_height == 0:
        if original_width >= 1800:
            caption_height = 100
            text_buffer = 20
            font_size = 42
        elif original_width >= 1200:
            caption_height = 75
            text_buffer = 15
            font_size = 32
        else:
            caption_height = 50
            text_buffer = 10
            font_size = 21

    new_width = original_width
    new_height = original_height + caption_height

    # Make new image with original dimensions but more height to allow for caption at bottom
    new_img = Image.new(mode = "RGB", size = (new_width, new_height), color = (60, 60, 60))

    # Paste original image onto new image
    offset = (0, 0)
    new_img.paste(img, offset)

    # Draw species name
    draw_species = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial_bold.ttf", font_size)
    draw_species.text((text_buffer, new_height - caption_height*0.75), species_name, (181, 200, 210), font=font)

    # Measure species name text width
    species_name_width = draw_species.textlength(species_name, font=font)

    # Draw scientific name
    draw_scientific = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial_italic.ttf", font_size)
    draw_scientific.text((3*text_buffer + species_name_width, new_height - caption_height*0.75), scientific_name, (255, 255, 255), font=font)

    # Measure scientific name text width
    scientific_name_width = draw_scientific.textlength(scientific_name, font=font)

    # Draw photographer name
    draw_photographer = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial_bold.ttf", font_size)
    draw_photographer.text((5*text_buffer + species_name_width + scientific_name_width, new_height - caption_height*0.75), f"© {photographer_name}", (255, 255, 255), font=font)

    # Measure photographer name text width
    photographer_name_width = draw_photographer.textlength(f"© {photographer_name}", font=font)

    # Draw Macaulay Library
    draw_library = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial.ttf", font_size)
    draw_library.text((7*text_buffer + species_name_width + scientific_name_width + photographer_name_width, new_height - caption_height*0.75), "Macaulay Library", (157, 157, 157), font=font)

    # Measure Macaulay Library text width
    library_width = draw_library.textlength("Macaulay Library", font=font)

    # Draw eBird
    draw_ebird = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("fonts/arial.ttf", font_size)
    draw_ebird.text((9*text_buffer + species_name_width + scientific_name_width + photographer_name_width + library_width, new_height - caption_height*0.75), "eBird", (157, 157, 157), font=font)

    # Measure eBird text width
    ebird_width = draw_ebird.textlength("eBird", font=font)

    # Check if total text width is too long
    total_text_width = 9*text_buffer + species_name_width + scientific_name_width + photographer_name_width + library_width + ebird_width

    if total_text_width >= original_width:
        caption_height = round(caption_height * 0.8)
        text_buffer = round(text_buffer * 0.8)
        font_size = round(font_size * 0.8)
        return add_caption(img, species_name, scientific_name, photographer_name, caption_height, text_buffer, font_size)

    return new_img