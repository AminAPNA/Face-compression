# This bash script creates movies from the Movie Frames created by the python scripts.
# The script searches for the frames in the MovieFrames folder where the frames for each movie are located in a separate subfolder.
# The MovieFrames folder should also contain a file ConcatInput.txt that is used as input to the ffmpeg command.
# The movies are stored in the Movies folder

# For each subfolder in the MovieFrames folder
for d in MovieFrames/*; do
    # Check if this is actually a folder
    if [ ! -d $d ]; then
        continue
    fi

    # Get the name of the subfolder
    dir=${d##*/}
    
    # Copy the ConcatInput.txt into the folder
    cp MovieFrames/ConcatInput.txt MovieFrames/$dir/

    # Change to the folder
    cd MovieFrames/$dir/

    # Create the movie
    ffmpeg -f concat -i ConcatInput.txt -c:v libx264 -r 30 ../../Movies/$dir.mp4

    # Change back to the main folder
    cd ../../
done