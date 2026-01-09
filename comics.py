import requests
import os
import telegram
import random
import argparse
from dotenv import load_dotenv 
from image_downloader import save_response_content, get_file_extension


def fetch_random_comic(random_number, directory):
    url = f'https://xkcd.com/{random_number}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()
    comics = response.json()

    filename_url = comics['img']
    comment = comics['alt']

    file_extension = get_file_extension(filename_url)
    filename = f'comic{random_number}{file_extension}'
    filepath_to_comics = os.path.join(directory, filename)

    response_comic_image = requests.get(filename_url)
    response_comic_image.raise_for_status()

    save_response_content(response_comic_image, filepath_to_comics)

    return filename, comment


def publish_for_telegram(directory, photo, comment, tg_comics_token, tg_chat_id):
    bot = telegram.Bot(token=tg_comics_token)
    filepath_to_comics = os.path.join(directory, photo)
    bot.send_document(chat_id=tg_chat_id, document=open(filepath_to_comics, 'rb'))
    bot.send_message(chat_id=tg_chat_id, text=comment)
    os.remove(filepath_to_comics)


def main():
    default_directory = os.path.join(os.path.dirname(__file__), 'images')

    parser = argparse.ArgumentParser(description="""Скачивает случайный комикс и публикует её в канал.""")
    parser.add_argument('--directory', type=str, default=default_directory)
    args = parser.parse_args()
    directory = args.directory
    os.makedirs(directory, exist_ok=True)

    load_dotenv()
    tg_comics_token = os.environ["TELEGRAM_COMICS_TOKEN"]
    tg_chat_id = os.environ["TELEGRAM_ID"]

    comic_url = 'https://xkcd.com/info.0.json'
    response = requests.get(comic_url)
    response.raise_for_status()
    comics_amount = response.json()['num']

    random_number = random.randint(1, comics_amount)
    filename, comment = fetch_random_comic(random_number, directory)
    publish_for_telegram(directory, filename, comment, tg_comics_token, tg_chat_id)


if __name__ == '__main__':
    main()