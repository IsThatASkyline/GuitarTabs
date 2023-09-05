# GuitarTabs

[![wakatime](https://wakatime.com/badge/user/60b3df07-9c18-4363-8c82-95a353ff7e15/project/02a2c739-df79-4c42-a72e-3a0b124e60bf.svg)](https://wakatime.com/badge/user/60b3df07-9c18-4363-8c82-95a353ff7e15/project/02a2c739-df79-4c42-a72e-3a0b124e60bf)

Приложение для гитаристов

Позволяет смотреть текст и аккорды для песен.


Основной функционал: 
- редактор музыкальных групп и песен,
- просмотр всех песен,
- просмотр всех песен исполнителя,
- поиск песен по названию, 
- добавление песен в 'Избранное' для более быстрого доступа к ним, 
- просмотр аппликатур аккордов, которые присутствуют в выбранной песне


## Установка и запуск:
```shell
git clone https://github.com/artklk12/GuitarTabs.git
cd GuitarTabs
```
Создайте файл .env и заполните его по примеру из .envExample 

### С помощью Poetry
```shell
pip install poetry==1.5.1
poetry install
alembic upgrade head
poetry run guitar-tgbot
```
### С помощью Docker
```shell
docker build --tag guitar_bot .
docker run guitar_bot
```
