# Macaulay Library Image Captioner
Command-line based tool to add captions including species name, scientific name and photographer name to Macaulay Library images when provided with a valid Macaulay Library asset link.

Example with https://macaulaylibrary.org/asset/647220543 below:

![Original vs Captioned Image](examples/647220543_example.png "Original vs Captioned Image")

## 1. Requirements
-   Python 3.13.5 (Latest version should be fine)
-   [Pillow 12.0.0](https://pypi.org/project/pillow/)
Install Pillow via `pip install pillow`

## 2. Usage
All of the following commands must be run from the **root directory**.

To process one Macaulay Library asset link, run the following, and the captioned image will be saved in the root directory.
```
python3 captioner.py link
```

To process multiple Macaulay Library asset links, there are two choices. 

The first way is to provide several links in the command line arguments, as following, where all captioned images will be saved in a created directory in the root directory.
```
python3 captioner.py link1 link2 link3
```

The second way is to provide a txt file containing one link per line, and providing the txt file name as a single command line argument, as following. The same result as above will be achieved.
```
python3 captioner.py links.txt
```
where the txt file has format:
```
link1
link2
link3
```


## 3. Additional Notes
-   When using multiple command line arguments to parse several links, be aware that any txt file in the program directory named `temp.txt` will be irreverssably overwritten. This is a default value and can be changed by editing the constant `TEMPORARY_TXT_NAME` in `captioner.py`.
-   The name of the directory images are saved in, if several images exist, is stored in the constant `DIRECTORY_NAME` in `captioner.py`. The default name is "captioned".
-   Macaulay Library stores several images of differing quality. The quality of image used from Macaulay Library is the one of 2400px width. If such a high quality image does not exist, the next highest quality image is used. 
-   All images are saved in PNG format, named by their "asset ID" (the number at the end of a Macaulay Library asset link).
-   Because of Pillow's image handling, the original image's colours may be slightly altered, as seen in the example.
-   The fonts used for the captioning are Arial, Arial Italics, and Arial Bold, stored in the directory `fonts`. 
-   This tool does NOT use eBird API, and is liable to break if Cornell updates their web UI.