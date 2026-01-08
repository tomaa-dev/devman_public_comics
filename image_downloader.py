import os
from urllib.parse import urlsplit, unquote


def create_directory(directory):
    os.makedirs(directory, exist_ok=True)


def download_the_image(response, filepath):
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_file_extension(url):
    path = urlsplit(url).path
    filename, file_extension = os.path.splitext(unquote(path))
    return file_extension