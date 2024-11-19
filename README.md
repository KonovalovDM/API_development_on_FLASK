# API_development_on_FLASK
 API_development_on_FLASK

Отличная инструкция!!!

Код представляет собой простое веб-приложение, использующее Flask и SQLAlchemy <br>
для управления пользователями и публикациями. Оно включает в себя создание, чтение, обновление и удаление (CRUD)<br>
операций для пользователей и публикаций с использованием API на Flask.

Этот код создает REST API для блога с использованием Flask.<br>
Вот краткая инструкция по запуску:

### Инструкция по запуску
1. Необходимые зависимости в файле requirements.txt, устанавливаем все сразу:
 ```bash
    pip install requirements.txt
````
Можно делать по отдельности
2. Установите необходимые зависимости:
   ```bash
   pip install Flask Flask-SQLAlchemy
   ```
3. Запустите приложение:
   ```bash
   python app.py
   ```
4. Приложение будет доступно по адресу `http://127.0.0.1:5000`.

### Примеры запросов:
- **Создать пользователя (POST `/users`)**:
   ```json
   {
     "username": "example_user"
   }
   ```
- **Создать пост (POST `/posts`)**:
   ```json
   {
     "title": "My First Post",
     "content": "This is the content of the first post.",
     "user_id": 1
   }
   ```
- **Прочитать все посты (GET `/posts`)**.
- **Прочитать пост по ID (GET `/posts/1`)**.
- **Изменить пост (PUT `/posts/1`)**:
   ```json
   {
     "title": "Updated Title",
     "content": "Updated content"
   }
   ```
- **Удалить пост (DELETE `/posts/1`)**.
