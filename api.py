"""Тут мы достаём из БД сценарии и формируем запросы и ответы"""

import pytest 
import configparser
from db import cursor

cfg = configparser.ConfigParser()
cfg.read('api.ini')
cfg = cfg['api']

class Request:
    def __init__(self, url="", params={}):
        self.url = url
        self.params = params

class Response:
    def __init__(self, status=200):
        self.status = status

class Scenario:
    def __init__(self, api="", request=None, response=None):
        self.api = api
        self.request = request
        self.response = response

def get_scenarios():
    """Собираем сценарии из таблиц БД
    Для разных методов тут будет наверняка разный сбор, но пока всё в кучу
    """

    arr = []
    with cursor() as cur:
        cur.execute(
            "SELECT f.feature, s.sc_id, s.ft_id, s.description, s.msisdn, s.account, s.\"startDateTime\", s.\"endDateTime\", s.\"isPositive\"\
            FROM public.\"Scenarios\" as s, public.\"Features\" as f\
            WHERE s.ft_id = f.ft_id\
              AND f.feature = 'fingate/account'\
            "
        )
        for rec in cur:
            rq = Request(url=cfg[rec['feature']],params={'msisdn': rec['msisdn'], 'startDateTime': rec['startDateTime'], 'endDateTime': rec['endDateTime']})
            re = Response(status=(200 if rec['isPositive'] is True else 400))
            arr.append(
                pytest.param(
                    Scenario(
                        api=rec['feature'],
                        request=rq,
                        response=re
                    ),
                    id=f"feature={rec['ft_id']} scenario={rec['sc_id']}" # будет кастомное имя теста
                )
            )
    print(arr)
    return arr
