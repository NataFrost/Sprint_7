import importlib

from src.client.courier_routs import CourierAPIClient
from src.client.order_routs import OrderAPIClient


def setup_clients(env):
    CourierAPIClient.host = env.courier_api
    OrderAPIClient.host = env.order_api

#c гибким запуском на разных окружених еще буду разбираться, но даже так переключение работает
def setup_config(config, env='dev'):
    env = importlib.import_module('src.config.dev')
    #env = importlib.import_module('src.config.test')
    setup_clients(env.EndpointUrl)

