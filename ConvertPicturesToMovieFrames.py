# This program reads images and converts them to movie frames. The movie frames are sorted per picture
# The program reads the pictures from two folders: OrigImages and CompressedImages.
# The original pictures are in the OrigImages folder. 
# The CompressedImages folder stores the compressed images with the name "<image_name>_compress_<amount_of_singular_values>.jpg"
# The output is put in the folder MovieFrames, where a subfolder is created for each picture.
# The movie frames are named "image-<number>.jpg" where <number> is the order in which the pictures need to be showed.
# This order is first the compressed images with increasing amount of singular values and then the original image.

import os
from PIL import Image, ImageDraw, ImageFont

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1200

MAX_IMAGE_WIDTH = 0.8*DISPLAY_WIDTH
MAX_IMAGE_HEIGHT = 0.75*DISPLAY_HEIGHT

FONT = ImageFont.truetype("NimbusSans-Bold.otf", 75)
TEXT = "Can you guess the compressed celebrity?"

Y_OFFSET_TEXT = 60
TEXT_IMAGE_GAP = 0.065*DISPLAY_HEIGHT

AM_SING_VALUES_WANTED = [2, 4, 6, 8, 12, 16, 24, 32, 64]

def createMoveFrame(imagePath):
    img = Image.new(mode="RGB", size=(DISPLAY_WIDTH,DISPLAY_HEIGHT), color=(36,36,36))

    # Draw the text on the image
    draw = ImageDraw.Draw(img)
    textWidth, textHeight = draw.textsize(TEXT, font=FONT)

    # Coordinates for text such that it is centered in the x direction
    textX = (DISPLAY_WIDTH - textWidth) // 2
    draw.text((textX, Y_OFFSET_TEXT), TEXT, fill=(220, 228, 238), font=FONT)

    # Insert the image on the screen
    overlayImage = Image.open(imagePath)

    # Resize the image to fit the screen
    if overlayImage.width > MAX_IMAGE_WIDTH or overlayImage.height > MAX_IMAGE_HEIGHT:
        overlayImage.thumbnail((MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT))
    elif overlayImage.width < MAX_IMAGE_WIDTH and overlayImage.height < MAX_IMAGE_HEIGHT:
        aspectRatio = min(MAX_IMAGE_WIDTH/overlayImage.width, MAX_IMAGE_HEIGHT/overlayImage.height)
        overlayImage = overlayImage.resize((int(overlayImage.width*aspectRatio), int(overlayImage.height*aspectRatio)))
        
    # Calculate the coordinates of the image on the screen
    imageX = (DISPLAY_WIDTH - overlayImage.width) // 2
    imageY = int(Y_OFFSET_TEXT + textHeight + TEXT_IMAGE_GAP)

    # Draw the image on the screen
    img.paste(overlayImage, (imageX, imageY))

    return img

if __name__ == "__main__":
    # Create the MovieFrames folder
    if not os.path.exists("MovieFrames"):
        os.makedirs("MovieFrames")

    # For each file in the OrigImages folder, create a subfolder of the same name in the MovieFrames folder
    for file in os.listdir("OrigImages"):
        # Get path without extension
        path = file.split(".")[0]

        # Create the subfolder
        if not os.path.exists("MovieFrames/"+path):
            os.makedirs("MovieFrames/"+path)

    # Convert each file in the compressed images folder to a movie frame
    for file in os.listdir("CompressedImages"):
        # Get path without extension
        path = file.split(".")[0]

        # Create the movie frame
        img = createMoveFrame("CompressedImages/"+file)

        # Get the image number
        nsVals = int(path.split("_")[2])
        imageNb = AM_SING_VALUES_WANTED.index(nsVals)+1

        # Get folder name
        path = path.split("_")[0]

        # Save the image
        img.save("MovieFrames/"+path+"/image-"+str(imageNb)+".jpg")

    # Convert each file in the original images folder to a movie frame
    for file in os.listdir("OrigImages"):
        # Get path without extension
        path = file.split(".")[0]

        # Create the movie frame
        img = createMoveFrame("OrigImages/"+file)

        # Get the image number
        imageNb = len(AM_SING_VALUES_WANTED)+1

        # Save the image
        img.save("MovieFrames/"+path+"/image-"+str(imageNb)+".jpg")