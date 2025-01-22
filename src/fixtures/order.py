import pytest

from src.client.order_routs import OrderAPIClient
from src.data.order_data import OrderData


@pytest.fixture
def order_api_client():
    client = OrderAPIClient()
    return client


# фикстура создает ордер и возвращает его номер по трэку
@pytest.fixture(scope='function')
def order_id(order=OrderData.ORDER_DATA):
    track = OrderAPIClient().post_v1_orders(data=order, status=201)
    order = OrderAPIClient().get_v1_orders_track(data=track, status=200)
    return order["order"]["id"]


# фикстура создает ордер и возвращает его track
@pytest.fixture(scope='function')
def track(order=OrderData.ORDER_DATA):
    track = OrderAPIClient().post_v1_orders(data=order, status=201)
    return track


# фикстура создает ордер, получает его номер по трэку и назначает его курьеру
@pytest.fixture(scope='function')
def order_id_accepted(prepare_courier_default, order=OrderData.ORDER_DATA):
    track = OrderAPIClient().post_v1_orders(data=order, status=201)
    order = OrderAPIClient().get_v1_orders_track(data=track, status=200)
    data = [order["order"]["id"], prepare_courier_default]
    OrderAPIClient().put_v1_orders_accept(status=200, data=data)
    return order["order"]["id"]


