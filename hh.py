import os
import json
from googleapiclient.discovery import build


class HeadHunterAPI:
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('HH_API_KEY')

    # создать специальный объект для работы с API
    hh = build('hh', 'v3', developerKey=api_key)
