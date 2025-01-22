from src.client.client import RequestCustom
import allure


class OrderAPIClient:
    host = None

    @allure.step("Вызвать сервис с параметрами: {path}, {data}")
    def post_v1_orders(self, path="api/v1/orders", data=None, status=200):
        url = f"{self.host}{path}"
        return RequestCustom().make_request_for_check('post', url, status=status, data=data)

    @allure.step("Вызвать сервис с параметрами: {path}, {data}")
    def get_v1_orders(self, path="api/v1/orders", data=None, status=200):
        url = f"{self.host}{path}"
        return RequestCustom().make_request_for_check('get', url, status=status, data=data)

    @allure.step("Вызвать сервис с параметрами: {path}, {data}")
    def put_v1_orders_accept(self, path="api/v1/orders/accept", data=None, status=200):
        url = f"{self.host}{path}/{str(data[0])}"
        put_params = {"courierId": data[1]['id']}
        return RequestCustom().make_request_for_check('put', url, status=status, data=put_params)

    @allure.step("Вызвать сервис с параметрами: {path}, {data}")
    def get_v1_orders_track(self, path="api/v1/orders/track", data=None, status=200):
        get_params = {"t": data["track"]}
        url = f"{self.host}{path}"
        return RequestCustom().make_request_for_check('get', url, status=status, data=get_params)

    @allure.step("Вызвать сервис с параметрами: {path}, {data}")
    def get_v1_orders_list(self, path="api/v1/orders", data=None, status=200):
        url = f"{self.host}{path}"
        return RequestCustom().make_request_for_check('get', url, status=status, data=data)
