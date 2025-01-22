import allure
import requests
import json
import pytest

from src.data.courier_data import CourierData
from src.client.courier_routs import CourierAPIClient


class TestCourierCreate:

    @allure.title("Проверка создания курьера")
    @pytest.mark.parametrize('courier', [CourierData.COURIER_DATA_1, CourierData.COURIER_DATA_2])
    def test_create_courier_201(self, courier_del, courier):
        response = CourierAPIClient().post_v1_courier(status=201, data=courier)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert response == {'ok': True}
            allure.attach(f'Response message: {response}, Expected message: {{"ok": True}} ',
                          name="Детали проверки",
                          attachment_type=allure.attachment_type.TEXT
                          )

    @allure.title("Проверка создания курьера, с логином уже существующим в системе")
    @pytest.mark.parametrize('courier', [CourierData.COURIER_DATA_1])
    def test_create_courier_with_the_same_login_409(self, prepare_courier, courier):
        response = CourierAPIClient().post_v1_courier(status=409, data=courier)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "Этот логин уже используется. Попробуйте другой." in response['message']

    @allure.title("Проверка, что курьер не создается, если не заданы все обязательные поля")
    @pytest.mark.parametrize('courier', CourierData.COURIER_INVALID_DATA)
    def test_create_courier_no_mandatory_fields_400(self, courier_api_client, courier):
        response = courier_api_client.post_v1_courier(status=400, data=courier)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "Недостаточно данных для создания учетной записи" in response['message']


class TestCourierLogin:

    @allure.title("Проверка, что курьер может залогиниться")
    @pytest.mark.parametrize('courier', [CourierData.COURIER_DATA_1, CourierData.COURIER_DATA_2])
    def test_login_courier_200(self, prepare_courier, courier):
        login_data = {"login": courier["login"], "password": courier["password"]}
        response = CourierAPIClient().post_v1_courier_login(data=login_data, status=200)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "id" in response and response["id"] > 0

    @allure.title("Проверка, что курьер не может залогиниться с неверным паролем")
    @pytest.mark.parametrize('courier', [CourierData.COURIER_DATA_1])
    def test_login_courier_invalid_password_404(self, prepare_courier, courier):
        login_data = {"login": courier["login"], "password": "invalid_password"}
        response = CourierAPIClient().post_v1_courier_login(data=login_data, status=404)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "Учетная запись не найдена" in response['message']

    @allure.title("Проверка, что курьер не может залогиниться с неверным логином")
    @pytest.mark.parametrize('courier', [CourierData.COURIER_DATA_1])
    def test_login_courier_invalid_login_404(self, prepare_courier, courier):
        login_data = {"login": "invalid_login", "password": courier["password"]}
        response = CourierAPIClient().post_v1_courier_login(data=login_data, status=404)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "Учетная запись не найдена" in response['message']

    @allure.title("Проверка, что нельзя залогиниться с несуществующим пользователем")
    def test_login_unknown_courier_404(self, courier_api_client):
        login_data = {"login": "unknown_courier", "password": "Unknown_password"}
        response = courier_api_client.post_v1_courier_login(status=404, data=login_data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "Учетная запись не найдена" in response['message']

    @allure.title("Проверка, что курьер не может залогиниться, если не заданы все обязательные поля")
    @pytest.mark.parametrize('courier', CourierData.COURIER_INVALID_LOGIN_DATA)
    def test_login_courier_no_mandatory_fields_400(self, courier_api_client, courier):
        response = courier_api_client.post_v1_courier_login(status=400, data=courier)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "Недостаточно данных для входа" in response['message']


class TestCourierDelete:

    @allure.title("Проверка, что курьера можно удалить")
    def test_delete_courier_200(self, courier_id):
        data = json.dumps(courier_id)
        response = CourierAPIClient().delete_v1_courier_by_id(status=200, data=data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert response == {'ok': True}
            allure.attach(f'Response message: {response}, Expected message: {{"ok": True}} ',
                          name="Детали проверки",
                          attachment_type=allure.attachment_type.TEXT
                          )

    @allure.title("Проверка, что нельзя удалить курьера с несуществующим id")
    @pytest.mark.parametrize('courier', CourierData.COURIER_UNKNOWN_ID)
    def test_delete_courier_unknown_id_404(self, courier):
        data = json.dumps(courier)
        response = CourierAPIClient().delete_v1_courier_by_id(status=404, data=data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "Курьера с таким id нет." in response["message"]

    @allure.title("Проверка, что нельзя удалить курьера без id")
    @pytest.mark.parametrize('courier', CourierData.COURIER_INVALID_ID)
    def test_delete_courier_invalid_id_404(self, courier):
        data = json.dumps(courier)
        response = CourierAPIClient().delete_v1_courier_by_id(status=404, data=data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "Not Found" in response["message"]

