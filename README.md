# FaceCompression NUMA Demo

This is a simple demo that shows how the SVD can be used to compress images. The demo consists of two parts: a GUI and code that creates Movies.

## GUI

The GUI is a simple interactive demo. On the left side of the screen it shows a live camera feed and a button to take a picture. After a countdown the picture is taken, and decomposed using the SVD. Then, the right side of the screen will show the truncated SVD approximation of the picture with increasing amount of singular values used. Some other stats, like the compression ratio are also shown.

To run the GUI, first update the parameters in the [GUI.py](./GUI.py) file and then run it with python3.

## Movie creator

There is also the possibility to create some movies that show the SVD compression of arbitrary pictures. This is done using multiple python and bash scripts.

First, place the images you wish to make a video for in a folder called `OrigImages` and create a second folder `CompressedImages`. Then, the script [ConvertPicturesToCompressed.py](./ConvertPicturesToCompressed.py) can convert the original pictures to an SVD compressed version. The parameters at the top of this script allow you to change the amount of compressed pictures and the amount of singular values used for this picture. 

Secondly, these compressed images need to be converted to frames of a movie. This is done using the [ConvertPicturesToMovieFrames.py](./ConvertPicturesToMovieFrames.py) script. The aspect ratio of the movie and other settings can be changed at the top of the file. This script automatically pulls all the required pictures from the `OrigImages` and `CompressedImages` folders and put them in the `MovieFrames` folder. This folder will contain a subfolder for each original image.

Finally, you have to create a movie for each of the original images. To do this, you will first have to create a concatenate demuxer for ffmpeg. The documentation for this can be read in the [ffmpeg documentation](https://ffmpeg.org/ffmpeg-formats.html#concat). This file tells ffmpeg how much time each frame must be displayed. An example for the default configuration is:
```
file 'image-1.jpg'
duration 2
file 'image-2.jpg'
duration 2
file 'image-3.jpg'
duration 2
file 'image-4.jpg'
duration 2
file 'image-5.jpg'
duration 2
file 'image-6.jpg'
duration 2
file 'image-7.jpg'
duration 1.5
file 'image-8.jpg'
duration 1.5
file 'image-9.jpg'
duration 1.5
file 'image-10.jpg'
duration 3
file 'image-10.jpg'
```

You have to place this content in a file called `ConcatInput.txt` in the `MovieFrames` folder. Then you need to create a folder named `Movies`. Finally, you can run the [CreateMovies.sh](./CreateMovies.sh) script that will create all required movies and put them in the `Movies` folder.