import logging
import os

from app.config import Config


def clear_directories():
    try:
        for file in os.listdir(Config.DOWNLOADS_PATH):
            if file != 'README.md':
                os.remove(os.path.join(Config.DOWNLOADS_PATH, file))
        for file in os.listdir(Config.UPLOADS_PATH):
            if file != 'README.md':
                os.remove(os.path.join(Config.UPLOADS_PATH, file))
    except FileNotFoundError:
        return logging.error('No such directory')
    logging.info("Directories was cleaned.")
