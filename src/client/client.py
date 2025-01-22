import json

import allure
import pytest
import requests
from requests import HTTPError

from src.config.dev import HEADERS


class RequestCustom:

    def __init__(self):
        self.response = 'Error'

    def update_headers(self, additional_headers):
        default_headers = HEADERS
        if additional_headers:
            default_headers.update(additional_headers)
        return default_headers

    def make_request(self, req_type, url, data, headers):
        if req_type in ('get', 'delete', 'put'):
            response = getattr(requests, req_type)(url, params=data, headers=headers)
        else:
            response = getattr(requests, req_type)(url, data=json.dumps(data), headers=headers)
        return response

    def make_request_for_check(self, req_type, url, status=200, data=None, headers=None):
        try:
            headers = self.update_headers(headers)
            self.response = self.make_request(req_type=req_type, url=url, data=data, headers=headers)
            msg = f'\nReal {self.response.status_code}\nExpected {status}\nData {data}\nResp {self.response.text}'
            with allure.step("Сравнение фактического и ожидаемого статус кода"):
                assert self.response.status_code == status, msg
                allure.attach(f'Response status: {self.response.status_code}, Expected status: {status} ',
                              name="Детали проверки",
                              attachment_type=allure.attachment_type.TEXT
                              )

            if 'application/json' in self.response.headers['Content-Type']:
                return self.response.json()
            else:
                return self.response.text

        except HTTPError as e:
            pytest.fail(f'Request error {e}\n{self.response.text}')
        except json.decoder.JSONDecodeError as e:
            pytest.fail(f'Request error {e}\n{self.response.text}')

