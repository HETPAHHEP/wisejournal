# Wisejournal — cоциальная сеть блогеров

*Проект Wisejournal.* Онлайн-сервис, в котором пользователи могут 
публиковать свои посты среди сообщества.

![Main page](docs/wisejournal-profile.png)

### 🔥 Возможности

- Опубликовать и редактировать свои посты с картинками
- Подписываться на авторов
- Комментировать отдельные публикации
- Просматривать страницу пользователя

### 👨‍💻 Технологии

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]


## ⚙ Начало Работы

Чтобы запустить копию проекта, следуйте инструкциям ниже.

### ⚠ Зависимости

- [Python 3.7+][Python-url]
- [Django 3.2](https://docs.djangoproject.com/en/3.2/)


### 🛠 Запуск в Dev-режиме

1. **Установите зависимости проекта**

    ```shell
    pip install -r requirements.txt
    ```

2. **Зафиксируйте миграции**

   ```bash
   ./manage.py migrate
   ```

3. **Создайте суперпользователя**

   ```bash
   ./manage.py createsuperuser
   ```

4. **Запустите dev-сервер**

    ```bash
    python manage.py runserver
    ```


---

<h5 align="center">
Автор проекта: <a href="https://github.com/HETPAHHEP">HETPAHHEP</a>
</h5>

<!-- MARKDOWN BADGES & URLs -->
[Python-badge]: https://img.shields.io/badge/Python-4db8ff?style=for-the-badge&logo=python&logoColor=%23ffeb3b

[Python-url]: https://www.python.org/

[Django-badge]: https://img.shields.io/badge/django-color?style=for-the-badge&logo=Django&logoColor=white&color=dark-green

[Django-url]: https://www.djangoproject.com
