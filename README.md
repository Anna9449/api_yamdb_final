# api_yamdb
api_yamdb
### Описание:

YaMDb API - это учебный проект, который собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Пользователи могут:
- оценивать и оставлять отзывы на произведения
- комментировать отзывы других пользователей

### Технологии:

- Python
- Django
- DRF
- JWT

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

Иван Барчунинов, Николай Шулькин, Анна Пестова
