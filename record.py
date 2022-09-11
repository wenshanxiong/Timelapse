#!/usr/bin/env python3
import subprocess
import argparse
import time
import sys
import os

    
SECONDS_PER_HOUR = 60 * 60
PROJECT_ROOT = '/home/pi/Documents/Timelapse'

parser = argparse.ArgumentParser()
   
parser.add_argument('-t', '--time', help='Interval between images in hours', type=str, required=True)
parser.add_argument('-m', '--max', help='Maxium number of images to keep. Ulimited by default', type=int, default=0)
args = parser.parse_args()

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)


interval = eval(args.time)

while True:
    if args.max > 0:
        list_of_files = os.listdir(f'{PROJECT_ROOT}/images')
        full_path = [f'{PROJECT_ROOT}/images/{x}' for x in list_of_files]

        if len(list_of_files) > args.max:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)

    subprocess.run(["fswebcam", "-r", "1920x1080", "--no-banner", f"{PROJECT_ROOT}/images/{time.ctime()}.jpg"])
    time.sleep(interval * SECONDS_PER_HOUR)