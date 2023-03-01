
Как запустить локально
---------------------------------------

```bash
$ pip3 install django django-channels uvicorn   # устанавливаем библиотеки
$ python3 manage.py migrate  # мигрируем базу
$ python3 -m uvicorn main.asgi:application 
```
После этого веб интерфейс будет доступен по адресу http://127.0.0.1:8000/chat/, 
вебсокет по ws://127.0.0.1:8000/ws/chat/{chatname}/.