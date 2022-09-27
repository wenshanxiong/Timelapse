#!/usr/bin/env bash
cd "${0%/*}"
export GOOGLE_APPLICATION_CREDENTIALS=/home/pi/Documents/Timelapse/service-account-secret.json
source .env/bin/activate
./record.py -m 90