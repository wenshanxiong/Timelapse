#!/usr/bin/env python3
import subprocess
from datetime import datetime
import os

curr_date = datetime.now().strftime('%F')
subprocess.run(
    [
        "ffmpeg", 
        "-framerate", "5", 
        "-pattern_type", "glob",
        "-i", "/home/pi/Documents/Timelapse/images/*.jpg",
        "-vf", "format=yuv420p",
        f"/home/pi/Documents/Timelapse/timelapse/{curr_date}.mp4"
    ]
)

# timelapse_name = os.listdir(f'{PROJECT_DIR}/timelapse')[0].split('.mp4')[0]
# [start_date, end_date] = timelapse_name.split(':')

# # stich with previous timelapse
# video_list = f"file '{PROJECT_DIR}/timelapse/{start_date}:{end_date}.mp4\nfile '{PROJECT_DIR}/timelapse/{end_date}:{curr_date}.mp4'"

# with open(f'{PROJECT_DIR}/video_list.txt', 'w') as f:
#     f.write(video_list)

# new_timelapse_path = f"{PROJECT_DIR}/timelapse/{start_date}:{curr_date}.mp4"
# subprocess.run([
#     "ffmpeg",
#     "-f", "concat",
#     "-safe", "0", 
#     "-i", f"{PROJECT_DIR}/video_list.txt", 
#     "-c", "copy",
#     new_timelapse_path,
#     "-y"
# ])

# if os.path.isfile(new_timelapse_path):
#     print("here")
#     # os.remove(f'{PROJECT_DIR}/timelapse/{start_date}:{end_date}.mp4')
#     # os.remove(f'{PROJECT_DIR}/timelapse/{end_date}:{curr_date}.mp4')