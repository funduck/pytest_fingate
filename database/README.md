# Админим локальный Postgres в докере
## Данные
папка `data` хранит данные базы и админки, но в репозиторий мы её не добавляем (.gitignore)

## Запуск и остановка
Стартует Postgres и pgAdmin на порту 5050
```
./run.sh
```
Остановка обоих контенеров
```
./stop.sh
```

## Экспорт БД
Бэкапит `test_db` в указанный файл в текущей папке
```
./backup_test_db.sh FILE
```

## Импорт БД
Стирает и воссоздаёт по бэкапу базу `test_db` из файла из текущей папки
```
./restore_test_db.sh FILE
```
