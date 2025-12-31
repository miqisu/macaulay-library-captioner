import urllib.request

# Extract html from a Macaulay Library link as a string
def extract_html_from_link(link):
    fp = urllib.request.urlopen(link)
    bytes = fp.read()

    html = bytes.decode("utf8")
    fp.close()

    # testing purpose only
    split = link.split("/")
    image_id = split[-1]
    
    return [html, image_id]

# Extracts highest quality main image link from Macaulay Library html and image ID
def get_image_link_from_html(html, image_id):
    # Can have 1200, 1800, 2400 after it
    image_link_starter = f"https://cdn.download.ams.birds.cornell.edu/api/v2/asset/{image_id}/"

    # If 2400 image exists
    if f"{image_link_starter}2400" in html:
        return f"{image_link_starter}2400"
    
    # If 1800 image exists
    if f"{image_link_starter}1800" in html:
        return f"{image_link_starter}1800"
    
    # If 1200 image exists
    if f"{image_link_starter}1200" in html:
        return f"{image_link_starter}1200"

# Extract species name, scientific name, photographer name from Macaulay Library html
def get_data_from_html(html):
    # Get species name
    temp = html.split("<span class=\"Heading-main\">")
    first_elem = temp[1]
    temp_split = first_elem.split("<")
    species_name = temp_split[0]

    # Get scientific name
    temp = html.split("<span class=\"Heading-sub Heading-sub--inline Heading-sub--sci\">")
    first_elem = temp[1]
    temp_split = first_elem.split("<")
    scientific_name = temp_split[0]

    # Get photographer name
    temp = html.split("© ")
    first_elem = temp[1]
    temp_split = first_elem.split(";")
    photographer_name = temp_split[0]
    # Some photographer names contain strings other than their name after a bar symbol
    if "|" in photographer_name:
        photographer_name = photographer_name.split("|")[0]

    return [species_name, scientific_name, photographer_name]