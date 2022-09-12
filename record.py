#!/usr/bin/env python3
from __future__ import print_function
import subprocess
import argparse
from time import localtime, strftime
import sys
import os
import glob
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

    
SECONDS_PER_HOUR = 60 * 60
PROJECT_ROOT = '/home/pi/Documents/Timelapse'

parser = argparse.ArgumentParser()
   
parser.add_argument('-m', '--max', help='Maxium number of images to keep. Ulimited by default', type=int, default=0)
args = parser.parse_args()

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.max > 0:
    list_of_files = os.listdir(f'{PROJECT_ROOT}/images')
    full_path = [f'{PROJECT_ROOT}/images/{x}' for x in list_of_files]
    if len(list_of_files) > args.max:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)

file_paths = glob.glob(f"{PROJECT_ROOT}/images/*.jpg")

creds, _ = google.auth.default()
try:
    # create drive api client
    service = build('drive', 'v3', credentials=creds)

    for path in file_paths:
        file_name = path.split('/')[-1]
        file_metadata = {
            'name': file_name,
            'parents': ['1vfJaSOC6n0Pk1gX0K1T3RnwuVxtpl8Gc']
        }
        media = MediaFileUpload(path,
                                mimetype='image/jpeg')
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
        print(F'Successfully uploaded {file_name} File ID: {file.get("id")}')
        os.remove(path)
        print('Removed loacl copy')

except HttpError as error:
    print(F'An error occurred: {error}')
    file = None


subprocess.run(["fswebcam", "-c", f"{PROJECT_ROOT}/fswebcam.conf", f"{PROJECT_ROOT}/images/{strftime('%Y-%m-%d %H:%M:%S', localtime())}.jpg"])