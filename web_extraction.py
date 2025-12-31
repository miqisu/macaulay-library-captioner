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
    filename = f"{image_id}.txt"
    with open(filename, "a") as f:
        f.write(html)
    
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


[html_test, image_id_test] = extract_html_from_link("https://macaulaylibrary.org/asset/204972611")
image_link = get_image_link_from_html(html_test, image_id_test)
print(image_link)