import pytest
import json

from src.client.courier_routs import CourierAPIClient
from src.data.courier_data import CourierData


@pytest.fixture
def courier_api_client():
    client = CourierAPIClient()
    return client


# фикстура c дефолтными данными курера: создает курьера, получает его id и удаляет курьера после завершения теста
@pytest.fixture(scope='function')
def prepare_courier_default(courier=CourierData.COURIER_DATA_1):
    login_data = {"login": courier["login"], "password": courier["password"]}
    #создаем нового курьера
    CourierAPIClient().post_v1_courier(data=courier, status=201)
    # вызываем метод login для получения id курьера
    courier_data = CourierAPIClient().post_v1_courier_login(data=login_data, status=200)
    yield courier_data
    #удаляем курьера
    CourierAPIClient().delete_v1_courier_by_id(data=json.dumps(courier_data))


# фикстура без дефолтных данных курьера: создает курьера, получает его id и удаляет курьера после завершения теста
@pytest.fixture(scope='function')
def prepare_courier(courier):
    login_data = {"login": courier["login"], "password": courier["password"]}
    #создаем нового курьера
    CourierAPIClient().post_v1_courier(data=courier, status=201)
    # вызываем метод login для получения id курьера
    courier_data = CourierAPIClient().post_v1_courier_login(data=login_data, status=200)
    yield courier_data
    #удаляем курьера
    CourierAPIClient().delete_v1_courier_by_id(data=json.dumps(courier_data))


# фикстура создает курьера и возвращает его id
@pytest.fixture(scope='function')
def courier_id(courier=CourierData.COURIER_DATA_2):
    login_data = {"login": courier["login"], "password": courier["password"]}
    CourierAPIClient().post_v1_courier(data=courier, status=201)
    courier_login = CourierAPIClient().post_v1_courier_login(data=login_data, status=200)
    return courier_login


# фикстура удаляет курьера после выполнения теста
@pytest.fixture(scope='function')
def courier_del(courier):
    yield
    login_data = {"login": courier["login"], "password": courier["password"]}
    courier_data = CourierAPIClient().post_v1_courier_login(data=login_data, status=200)
    CourierAPIClient().delete_v1_courier_by_id(data=json.dumps(courier_data))

