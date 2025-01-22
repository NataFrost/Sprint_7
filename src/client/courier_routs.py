from src.client.client import RequestCustom
import json
import allure


class CourierAPIClient:
    host = None

    @allure.step("Вызвать сервис с параметрами: {path}, {data}")
    def post_v1_courier(self, path="api/v1/courier", data=None, status=200):
        url = f"{self.host}{path}"
        return RequestCustom().make_request_for_check('post', url, status=status, data=data)

    @allure.step("Вызвать сервис с параметрами: {path}, {data}")
    def post_v1_courier_login(self, path="api/v1/courier/login", data=None, status=200):
        url = f"{self.host}{path}"
        return RequestCustom().make_request_for_check('post', url, status=status, data=data)

    @allure.step("Вызвать сервис с параметрами: {path}, {data}")
    def delete_v1_courier_by_id(self, path="api/v1/courier/", data=None, status=200):
        courier_id = json.loads(data)["id"]
        url = f"{self.host}{path}{courier_id}"
        return RequestCustom().make_request_for_check('delete', url, status=status, data=data)
