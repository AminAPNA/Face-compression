import cv2
import time
import numpy as np
from aux_functions import SVD_compress

vc = cv2.VideoCapture(2)

# Setting a custom resolution (1920 x 1080)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set width
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Set height

# # Setting a custom resolution (1240 x 720)
# vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1240)  # Set width
# vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height

# Get frame from camera
rval, frame = vc.read()

if not rval:
    raise ValueError("Camera feed not available")

# Create window
# cv2.namedWindow("preview")
cv2.namedWindow("preview", cv2.WINDOW_NORMAL)  # Make window resizable

# Comment both the following lines if you don't want to save/load pictures!

# Save to a file (if previous code is not commented)
# np.save("frame.npy", frame)

# # Load saved picture (if previous code is commented)
# frame = np.load("frame.npy")

s = 70 # compression parameter (i.e., number of singular values in the compression)


# Compress the image (first s largest singular values in R,G,B components)
frame_compress = SVD_compress(frame,s)

# Show frame
# cv2.imshow("preview", frame) # show original picture
cv2.imshow("preview", frame_compress) # show compressed picture

# Resize the window to specific width and height
# Change values to fit the screen, possibly with the same ratio of the original resolution
cv2.resizeWindow("preview", 1920, 1080) 

# Wait for esc key press
while True:
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        cv2.destroyWindow("preview")
        break
    # Break if the window is manually closed (MR: for my sanity since I kept manually closing it lol)
    if cv2.getWindowProperty("preview", cv2.WND_PROP_VISIBLE) < 1:
        break


