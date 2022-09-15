#!/usr/bin/env python3
from __future__ import print_function
import subprocess
import argparse
from time import localtime, strftime
import sys
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


SECONDS_PER_HOUR = 60 * 60
PROJECT_ROOT = "/home/pi/Documents/Timelapse"

parser = argparse.ArgumentParser()

parser.add_argument(
    "-m",
    "--max",
    help="Maxium number of images to keep. Ulimited by default",
    type=int,
    default=0,
)
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.max > 0:
    list_of_files = os.listdir(f"{PROJECT_ROOT}/images")
    full_path = [f"{PROJECT_ROOT}/images/{x}" for x in list_of_files]
    if len(list_of_files) > args.max:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)



image_name = f"{strftime('%Y-%m-%d %H:%M:%S', localtime())}"
subprocess.run(
    [
        "fswebcam",
        "-c",
        f"{PROJECT_ROOT}/fswebcam.conf",
        f"{PROJECT_ROOT}/images/{image_name}.jpg",
    ]
)

creds, _ = google.auth.default()
try:
    # create drive api client
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': f'{image_name}.jpg',
        'parents': ['1vfJaSOC6n0Pk1gX0K1T3RnwuVxtpl8Gc']
    }
    media = MediaFileUpload(f'{PROJECT_ROOT}/images/{image_name}.jpg',
                            mimetype='image/jpeg')
    # pylint: disable=maybe-no-member
    service.files().create(body=file_metadata, media_body=media,
                                    fields='id').execute()
except HttpError as error:
    print(F'An error occurred: {error}')


with open("image_list.txt", "a") as f:
    f.write(f"file {PROJECT_ROOT}/images/{image_name}.jpg")
