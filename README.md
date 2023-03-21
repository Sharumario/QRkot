# Приложение QRKot_Spreadsheets
## Описание
QRkot - это API сервиса по сбору средств на различные целевые проекты: на медицинское   обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм   оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.  
Добавлено формирование отчёта по закрытым проектам. 
## Установка
Зарегистрируйтесь в Google Cloud Platform. Создайте проект и подключите к новому проекту:  
Google Drive API и Google Sheets API. Затем получите JSON-файл с ключом доступа к сервисному аккаунту.
Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone git@github.com:Sharumario/cat_charity_fund.git
```
```
cd cat_charity_fund/
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
* Если у вас Linux/macOS
    ```
    source venv/bin/activate
    ```
* Если у вас windows
    ```
    source venv/scripts/activate
    ```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Создаём .env файл
```
APP_TITLE=Благотворительный фонд поддержки котиков QRKot
APP_DESCRIPTION=Сервис для поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./qrkot.db
SECRET=<секретное слово>
FIRST_SUPERUSER_EMAIL=<email суперюзера>
FIRST_SUPERUSER_PASSWORD=<пароль суперюзера>
EMAIL = <ваш google email>
TYPE = <из JSON-файл с ключом доступа>
PROJECT_ID = <из JSON-файл с ключом доступа>
PRIVATE_KEY_ID = <из JSON-файл с ключом доступа>
PRIVATE_KEY = <из JSON-файл с ключом доступа>
CLIENT_EMAIL = <из JSON-файл с ключом доступа>
CLIENT_ID = <из JSON-файл с ключом доступа>
AUTH_URI = <из JSON-файл с ключом доступа>
TOKEN_URI = <из JSON-файл с ключом доступа>
AUTH_PROVIDER_X509_CERT_URL = <из JSON-файл с ключом доступа>
CLIENT_X509_CERT_URL = <из JSON-файл с ключом доступа>
```
Примените миграции командой:
```
alembic upgrade head
```
## Запуск и ендпоинты
Запуск производится через команду:
```
uvicorn app.main:app --reload
```
После запуска апи готово к работе
- http://127.0.0.1:8000 - API
- http://127.0.0.1:8000/docs - документация Swagger
- http://127.0.0.1:8000/redoc - документация ReDoc
- http://127.0.0.1:8000/auth/register - регистрация пользователя
- http://127.0.0.1:8000/auth/jwt/login - аутентификация пользователя
- http://127.0.0.1:8000/auth/jwt/logout - выход
- http://127.0.0.1:8000/users/me - получение и изменение данных пользователя
- http://127.0.0.1:8000/users/{id} - получение и изменение данных пользователя по id
- http://127.0.0.1:8000/charity_project/ - получение списка проектов и создание нового
- http://127.0.0.1:8000/charity_project/{project_id} - изменение и удаление проекта
- http://127.0.0.1:8000/donation/ - получение списка всех пожертвований и создание пожертвования
- http://127.0.0.1:8000/donation/my - получение списка всех пожертвований пользователя
- http://127.0.0.1:8000/google - Отчёт по скорости закрытия в GOOGLE таблице

## Над проектом работали:
[Шайхнисламов Марат](https://github.com/Sharumario/) при поддержке ЯндексПрактикума