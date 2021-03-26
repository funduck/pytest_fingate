"""Главный файл для pytest"""

import configparser
import os.path
import pytest
from api import get_scenarios
from db import connect, disconnect
from setup import warmup, clear

@pytest.fixture(scope="session",autouse=True)
def db_connections():
    """Принудительно откроем соединение с БД, используемой в тестах и не забудем его закрыть в конце"""
    connect()
    yield True
    disconnect()

@pytest.fixture(scope="session",autouse=True)
def initialize_fingate():
    """Прогрев Fingate данными для тестов"""
    cfg = configparser.ConfigParser()
    cfg.read('setup.ini')
    cfg = cfg['fingate']
    cfg["backups"] = os.path.abspath(cfg["backups"])
    cfg["uploads"] = os.path.abspath(cfg["uploads"])
    warmup(uploads=cfg["uploads"], backups=cfg["backups"], timeout=int(cfg["warmup_timeout"]))
    yield
    """И очищаем Fingate после себя"""
    clear()

def pytest_generate_tests(metafunc):
    """Заполняем сценарии из БД тестов"""
    if 'scenario' in metafunc.fixturenames:
        metafunc.parametrize('scenario', get_scenarios())
