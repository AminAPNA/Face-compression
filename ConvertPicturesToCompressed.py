# Program that reads an image, compresses it with the SVD and stores the image again for different amounts of singular values
# The images need to be provided in the folder "OrigImages" and the compressed images will be stored in the folder "CompressedImages"

import os
import sys
import imageio.v3 as iio
from aux_functions import *

# Amount of Singular values wanted
AM_SING_VALUES_WANTED = [2, 4, 6, 8, 12, 16, 24, 32, 64]

if __name__ == "__main__":
    # For each file in the OrigImages folder
    for file in os.listdir("OrigImages"):
        # Read the image
        origImage = iio.imread("OrigImages/"+file)

        # Get path without extension
        path = file.split(".")[0]

        # Compute the SVD of the image
        SVD = computeSVD(origImage)

        # Create output image
        floatOut = np.zeros_like(origImage, dtype=np.float64)

        # Create first image
        floatOut = addCompressedFactorsSVD(SVD, floatOut, 0, AM_SING_VALUES_WANTED[0])
        iio.imwrite("CompressedImages/"+path+"_compress_"+str(AM_SING_VALUES_WANTED[0])+".jpg", floatOut.clip(0, 255).astype(np.uint8))

        # Compress the image and save
        for i in range(1, len(AM_SING_VALUES_WANTED)):
            floatOut = addCompressedFactorsSVD(SVD, floatOut, AM_SING_VALUES_WANTED[i-1], AM_SING_VALUES_WANTED[i])
            iio.imwrite("CompressedImages/"+path+"_compress_"+str(AM_SING_VALUES_WANTED[i])+".jpg", floatOut.clip(0, 255).astype(np.uint8))