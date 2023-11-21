# DollarRateBot

Описание

Телеграм-бот, который определяет имя пользователя и приветствует его.
Регистрирует и возвращает список зарегистрированных пользователей из БД. 
Сообщает текущий курс доллара.
На основе pyTelegramBotAPI и Django.


Настройка

Перейти в папку проекта: cd bot
Создать виртуальное окружение: python -m venv venv
Установить зависимости: pip install -r requirements.txt


Создать и применить миграции:

cd botbiz
python manage.py makemigrations
python manage.py migrate


Запуск админки:

python manage.py runserver


Запуск бота:

python manage.py bot
