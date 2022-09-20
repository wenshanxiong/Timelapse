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
import logging
import util


SECONDS_PER_HOUR = 60 * 60

logging.basicConfig(
    filename='logs/record.log',
    format='[%(levelname)s] %(asctime)s %(message)s',
    level=logging.INFO
)
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--max", help="Maxium number of images to keep. Ulimited by default",
    type=int, default=0,
)
parser.add_argument("-d", "--dry-run", help="No upload to Google cloud", action='store_true')
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.max > 0:
    list_of_files = os.listdir(f"images")
    full_path = [f"images/{x}" for x in list_of_files]
    if len(list_of_files) > args.max:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)


try:
    image_name = f"{strftime('%Y-%m-%d %H:%M', localtime())}"
    subprocess.run(
        [
            "fswebcam",
            "-c",
            "fswebcam.conf",
            "--set",
            f"Exposure (Absolute)={util.auto_exposure()}",
            f"images/{image_name}.jpg",
        ]
    ).check_returncode()
except subprocess.CalledProcessError as err:
        logging.error(err.stderr)
        sys.exit(1)

if args.dry_run:
    creds, _ = google.auth.default()
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': f'{image_name}.jpg',
            'parents': ['1vfJaSOC6n0Pk1gX0K1T3RnwuVxtpl8Gc']
        }
        media = MediaFileUpload(f'images/{image_name}.jpg',
                                mimetype='image/jpeg')
        # pylint: disable=maybe-no-member
        service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
    except HttpError as error:
        logging.error(F'An error occurred: {error}')
        sys.exit(1)
