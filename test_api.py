"""Тесты API
Тут мы дёргаем API и проверяем результаты"""

import requests
import pytest

current_scenario = None
response = None

@pytest.fixture
def call_api(scenario):
    """Вызов API по сценарию, сценарии параметризуются, все зависящие тесты будут проверять этот же сценарий"""
    global current_scenario
    global response
    current_scenario = scenario

    print('calling api for scenario', scenario.request.url, scenario.request.params)
    
    response = requests.get(url=scenario.request.url, params=scenario.request.params)

def test_response_status(call_api):
    """Проверка статуса ответа по сценарию"""
    global current_scenario
    global response

    assert response.status_code == current_scenario.response.status
