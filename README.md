# api_yamdb
api_yamdb
### Описание:

YaMDb API - это учебный проект, который собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Пользователи могут:
- оценивать и оставлять отзывы на произведения
- комментировать отзывы других пользователей

### Технологии:

[![pre-commit](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3111/) 
[![pre-commit](https://img.shields.io/badge/Django-3.2-092E20?logo=django&logoColor=white)](https://docs.djangoproject.com/en/4.2/releases/3.2/)
[![pre-commit](https://img.shields.io/badge/Django_REST_framework-3.12-800000?logo=djangorestramework&logoColor=white)](https://www.django-rest-framework.org/community/3.12-announcement/)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:bikovshanin/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Документация к API:

Документация к API проекта доступна по ссылке
http://127.0.0.1:8000/redoc/

### Авторы

[![pre-commit](https://img.shields.io/badge/Ivan-Barchuninov-0000FF?logo=github&logoColor=white)](https://github.com/bikovshanin)
[![pre-commit](https://img.shields.io/badge/Nikolay-Shulkin-0000FF?logo=github&logoColor=white)](https://github.com/stanlyzera)
[![pre-commit](https://img.shields.io/badge/Anna-Pestova-0000FF?logo=github&logoColor=white)](https://github.com/Anna9449)
