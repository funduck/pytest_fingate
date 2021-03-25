"""Тест что фреймворк готов к работе"""

def test_setup(db_connections):
    assert db_connections is True
