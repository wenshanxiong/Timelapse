#!/usr/bin/env bash
# CURR_DATE=$(date +%Y-%m-%d)
# END_DATE=(${IN//;/ })

file = $(/home/pi/Documents/Timelapse/timelapse/*.mp4)
echo "${file##*/}"



# ffmpeg -framerate 5 -i ./images/%d.jpg -vf format=yuv420p timelapse1.mp4ffmpeg -framerate 5 -i ./images/%d.jpg -vf format=yuv420p timelapse1.mp4

# ffmpeg -framerate 5 -i ./images/%d.jpg -vf format=yuv420p timelapse1.mp4