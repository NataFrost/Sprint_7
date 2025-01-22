import os

from dotenv import load_dotenv

load_dotenv()

PATH = os.getenv('path')
HEADERS = {'accept': 'application/json', 'Content-Type': 'application/json'}


class EndpointUrl:
    #courier_api = f'http://{PATH}'
    courier_api = 'https://qa-scooter.praktikum-services.ru/'
    order_api = 'https://qa-scooter.praktikum-services.ru/'
