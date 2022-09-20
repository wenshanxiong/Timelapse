from __future__ import print_function

import io

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


def download_file(real_file_id):
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        topFolderId = real_file_id
        items = []
        pageToken = ""
        while pageToken is not None:
            response = service.files().list(q="'" + topFolderId + "' in parents", pageSize=1000, pageToken=pageToken, fields="nextPageToken, files(id, name)").execute()
            items.extend(response.get('files', []))
            pageToken = response.get('nextPageToken')

        items.sort(key=lambda x: x['name'])
        for idx, item in enumerate(items):
            file_id = item['id']
            request = service.files().get_media(fileId=file_id)
            file = io.FileIO(f'images/{idx}.jpg', 'wb')
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')


    except HttpError as error:
        print(F'An error occurred: {error}')


if __name__ == '__main__':
    download_file(real_file_id='1vfJaSOC6n0Pk1gX0K1T3RnwuVxtpl8Gc')