import customtkinter
import cv2
from PIL import Image

from aux_functions import *

# TODO: We could scale this to be higher, but this is slow for the current implementation
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

# Picture SIZES
PICTURE_WIDTH = 900
PICTURE_HEIGHT = 675

# First display size (Laptop screen)
FIRST_SCREEN_WIDTH = 1920
FIRST_SCREEN_HEIGHT = 1200

# Second display size (External monitor)
SECOND_SCREEN_WIDTH = 1920
SECOND_SCREEN_HEIGHT = 1080

# SVD Update parameters
SVD_UPDATE_TIME = 1000
SVD_SING_VECTORS_INCREASE = 2

FRAME_TIME = 30

FONT = cv2.FONT_HERSHEY_TRIPLEX
FONT_SCALE = 8
FONT_THICKNESS = 8

# Change this number to enable the camera you want to use. If you want to use the default webcam, it will probably be 0. To use the webcam on huey it is 4!
# On different machines you will have to change this number and see which works with trail and error.
vc = cv2.VideoCapture(2) 

# Setting a custom resolution
vc.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)  # Set width
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)  # Set height

class App(customtkinter.CTk):
    def __init__(self):
        customtkinter.CTk.__init__(self)
        self.title("SVD Photo Booth")

        # Create font
        self.font = customtkinter.CTkFont(family="Helvetica", size=20, weight="bold")

        # Configure the grid to center everything
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # We create a frame in which we put everything
        self.everything_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.everything_frame.grid(row=0, column=0)

        # Init place for camera feed
        self.feed = customtkinter.CTkLabel(self.everything_frame, text="", compound="top", font=self.font)
        self.feed.grid(row=0, column=0, padx=8, pady=8)
        self.iteration=0

        # Init place for picture that is taken
        self.picture = customtkinter.CTkLabel(self.everything_frame, text="", compound="top", font=self.font)
        self.picture.grid(row=0, column=1, padx=8, pady=8)

        # Init place for everything under the picture that is taken
        self.pictureInfoFrame = customtkinter.CTkFrame(self.everything_frame, fg_color="transparent")
        self.pictureInfoFrame.grid(row=1, column=1, padx=8, pady=8)

        # Init place for labels under picture that is taken
        self.pictureTextFrame = customtkinter.CTkFrame(self.pictureInfoFrame, fg_color="transparent")
        self.pictureTextFrame.grid(row=0, column=0, padx=8, pady=8)

        # Text for compressed and original amount of bytes
        self.pictureTextOriginal = customtkinter.CTkLabel(self.pictureTextFrame, text="", compound="top", font=self.font)
        self.pictureTextOriginal.grid(row=0, column=0, padx=20, pady=8)

        self.pictureTextCompressed = customtkinter.CTkLabel(self.pictureTextFrame, text="", compound="top", font=self.font)
        self.pictureTextCompressed.grid(row=0, column=1, padx=20, pady=8)

        # Init progress bar
        self.progress = customtkinter.CTkProgressBar(self.pictureInfoFrame, width=500, height=50)
        self.progress.set(0)
        self.progress.grid(row=1, column=0, padx=8, pady=8)

        # Init button to take picture
        self.button = customtkinter.CTkButton(self.everything_frame, text="Take Picture", command=self.takePicture, font=self.font, width=250, height=50)
        self.button.grid(row=1, column=0, padx=8, pady=8)

        # Add a textbox to overlay text on the progress bar
        self.progressText = customtkinter.CTkLabel(self.progress, text="0%", fg_color="transparent", bg_color="transparent", font=self.font)
        self.progressText.grid(row=0, column=0, padx=8, pady=8)

        # Countdown to take picture
        self.countdown = 0

        # SVD animation status
        self.SVDAnimationActive = False

        self.updateCamera(FRAME_TIME)

    def updateCamera(self, delay, event=None):
        self.feedImage = self.getImage()
        self.feed.configure(image=self.feedImage)
        # reschedule to run again in 1 second
        self.after(delay, self.updateCamera, FRAME_TIME)

    def getFrame(self):
        if not vc.isOpened():
            raise ValueError("Camera feed not available")

        rval, frame = vc.read()

        if not rval:
            raise ValueError("Camera feed could not be read")
        
        return frame


    def getImage(self):
        # this is where you get your image and convert it to 
        # a Tk PhotoImage. For demonstration purposes I'll
        # just return a static image
        frame = self.getFrame()
        
        
        # Add text on image
        if self.countdown > 0:
            text = str(self.countdown)
            textSize = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICKNESS)

            # Calculate text position such that it is centered
            textX = (frame.shape[1] - textSize[0][0]) // 2
            textY = (frame.shape[0] + textSize[0][1]) // 2

            cv2.putText(img=frame, text=text, org=(textX,textY),fontFace=FONT, fontScale=FONT_SCALE, color=(0,0,255), thickness=FONT_THICKNESS)

        im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = customtkinter.CTkImage(im, size=(PICTURE_WIDTH, PICTURE_HEIGHT)) 
        return image
            
        
    def takePicture(self):
        self.countdown = 3
        self.after(1000, self.countDown)

    def countDown(self):
        if self.countdown > 0:
            self.countdown -= 1
            self.after(1000, self.countDown)
        else:
            # Check if the SVD animation is already active, if this is the case we cancel the current animation
            if self.SVDAnimationActive:
                self.after_cancel(self.SVDAnimationAfterCall)
                self.SVDAnimationActive = False

            self.pictureFrame = self.getFrame()
            self.pictureFrameSVD = computeSVD(self.pictureFrame)
            self.pictureFrameCompressed = np.zeros_like(self.pictureFrame, dtype=np.float64)
            self.SVDAnimationActive = True
            self.showSVD(0, SVD_SING_VECTORS_INCREASE)

    def showSVD(self, nsValsStart, nsValsEnd):
        # Update the image with the new singular vectors
        self.pictureFrameCompressed = addCompressedFactorsSVD(self.pictureFrameSVD, self.pictureFrameCompressed, nsValsStart, nsValsEnd)

        # Show the new image
        im = Image.fromarray(cv2.cvtColor(self.pictureFrameCompressed.clip(0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB))
        self.pictureImage = customtkinter.CTkImage(im, size=(PICTURE_WIDTH, PICTURE_HEIGHT))

        self.picture.configure(image=self.pictureImage)

        # Calculate the original amount of bytes
        amBytesOriginal = float(VIDEO_WIDTH*VIDEO_HEIGHT*3)/1000.0
        self.pictureTextOriginal.configure(text="Original size: %5.2f Kb" % amBytesOriginal)

        # Calculate the compressed amount of bytes
        amBytesCompressed = float(nsValsEnd*(VIDEO_WIDTH+VIDEO_HEIGHT)*3)/1000.0
        self.pictureTextCompressed.configure(text="Compressed size: %5.2f Kb" % amBytesCompressed)

        # Update the progress bar
        maxSingVectors = min(self.pictureFrameCompressed.shape[0], self.pictureFrameCompressed.shape[1])
        self.progress.set(amBytesCompressed/amBytesOriginal)
        self.progressText.configure(text="%d%%" % (amBytesCompressed/amBytesOriginal*100))

        # Prepare next call if this is needed
        if (amBytesCompressed/amBytesOriginal < 1):
            self.SVDAnimationAfterCall = self.after(SVD_UPDATE_TIME, self.showSVD, nsValsEnd, min(nsValsEnd+SVD_SING_VECTORS_INCREASE, maxSingVectors))
        else:
            self.SVDAnimationActive = False

if __name__ == "__main__":
    app=App()

    # Set app to be fullscreen
    app.attributes("-fullscreen", True)
    
    # Bind the escape key to close the app
    app.bind("<Escape>", lambda e: app.destroy())

    # Put the app on the primary display
    app.geometry("%dx%d+%d+%d" % (SECOND_SCREEN_WIDTH, SECOND_SCREEN_HEIGHT, FIRST_SCREEN_WIDTH, FIRST_SCREEN_HEIGHT))
    
    app.mainloop()
