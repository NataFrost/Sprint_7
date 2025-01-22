import allure
import pytest

from src.data.order_data import OrderData
from src.client.order_routs import OrderAPIClient


class TestOrderCreate:

    @allure.title("Проверка создания ордера")
    @pytest.mark.parametrize('color', OrderData.COLOR)
    @pytest.mark.parametrize('order', [OrderData.ORDER_DATA])
    def test_create_order_different_colors_201(self, order_api_client, color, order):
        order["color"] = color
        response = order_api_client.post_v1_orders(status=201, data=order)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "track" in response and response["track"] > 0


class TestOrderAccept:

    @allure.title("Проверка принятия заказа курьером")
    def test_accept_order_200(self, prepare_courier_default, order_id):
        data = [order_id, prepare_courier_default]
        response = OrderAPIClient().put_v1_orders_accept(status=200, data=data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert response == {'ok': True}
            allure.attach(f'Response message: {response}, Expected message: {{"ok": True}} ',
                          name="Детали проверки",
                          attachment_type=allure.attachment_type.TEXT
                          )

    @allure.title("Проверка повторного принятия заказа курьером")
    def test_accept_order_duplicate_409(self, prepare_courier_default, order_id_accepted):
        data = [order_id_accepted, prepare_courier_default]
        response = OrderAPIClient().put_v1_orders_accept(status=409, data=data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert "Этот заказ уже в работе" in response["message"]

    @allure.title("Проверка принятия заказа курьером, если id заказа не существует")
    def test_accept_order_unknown_order_id_404(self, prepare_courier_default):
        order_id = 123456789
        data = [order_id, prepare_courier_default]
        response = OrderAPIClient().put_v1_orders_accept(status=404, data=data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert 'Заказа с таким id не существует' in response['message']

    @allure.title("Проверка принятия заказа курьером, если id заказа не указан")
    def test_accept_order_missed_order_id_404(self, prepare_courier_default):
        order_id = ''
        data = [order_id, prepare_courier_default]
        response = OrderAPIClient().put_v1_orders_accept(status=404, data=data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert 'Not Found' in response['message']

    @allure.title("Проверка принятия заказа курьером, если id курьера не указан")
    def test_accept_order_missed_courier_id_400(self, order_id):
        prepare_courier = {'id': ''}
        data = [order_id, prepare_courier]
        response = OrderAPIClient().put_v1_orders_accept(status=400, data=data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert 'Недостаточно данных для поиска' in response['message']

    @allure.title("Проверка принятия заказа курьером, если id курьера не существует")
    def test_accept_order_unknown_courier_id_404(self, prepare_courier_default, order_id):
        prepare_courier_unknown = {'id': prepare_courier_default["id"] + 1}
        data = [order_id + 1, prepare_courier_unknown]
        response = OrderAPIClient().put_v1_orders_accept(status=404, data=data)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert 'Курьера с таким id не существует' in response['message']


class TestOrderGet:

    @allure.title("Проверка списка ордеров с параметрами")
    @pytest.mark.parametrize('params', OrderData.PARAMS)
    def test_get_orders_list_with_parameters_200(self, order_api_client, params):
        response = order_api_client.get_v1_orders_list(status=200, data=params)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert len(response["orders"]) == params["limit"]


    @allure.title("Проверка получения заказа по его номеру")
    def test_get_orders_by_track_200(self, track):
        response = OrderAPIClient().get_v1_orders_track(data=track, status=200)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert len(response) == 1 and 'id' in response['order'] and response['order']['id'] > 0

    @allure.title("Проверка получения заказа с несуществующим номером")
    def test_get_orders_by_unknown_track_404(self):
        track = {"track": 00000}
        response = OrderAPIClient().get_v1_orders_track(data=track, status=404)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert 'Заказ не найден' in response['message']

    @allure.title("Проверка получения заказа без номера трека")
    def test_get_orders_by_empty_track_400(self):
        track = {"track": ""}
        response = OrderAPIClient().get_v1_orders_track(data=track, status=400)
        with allure.step("Сравнение фактического и ожидаемого результата"):
            assert 'Недостаточно данных для поиска' in response['message']

