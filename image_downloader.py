import os
from urllib.parse import urlsplit, unquote


def save_response_content(response, filepath):
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_file_extension(url):
    path = urlsplit(url).path
    filename, file_extension = os.path.splitext(unquote(path))
    return file_extension