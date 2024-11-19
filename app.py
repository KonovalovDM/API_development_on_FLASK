from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Настраиваем базу данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создаем объект для работы с базой данных
db = SQLAlchemy(app)

# Определяем модель User (Пользователь)
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)                           # Уникальный идентификатор пользователя
    username = db.Column(db.String(80), unique=True, nullable=False)       # Имя пользователя, должно быть уникальным и не может быть пустым

    posts = db.relationship('Post', backref='author', lazy=True)     # Связь один ко многим с моделью Post

# Определяем модель Post (Публикация)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)                            # Уникальный идентификатор публикации
    title = db.Column(db.String(120), nullable=False)                       # Заголовок публикации, не может быть пустым
    content = db.Column(db.Text, nullable=False)                            # Содержимое публикации, не может быть пустым
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Идентификатор пользователя, связанного с публикацией

# Создаем таблицы в базе данных
with app.app_context():
    db.create_all()

# Определяем маршрут для главной страницы
@app.route('/')
def home():
    return "Welcome to the API!"

# Точка доступа для создания нового пользователя
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()                                               # Получаем данные из запроса
    new_user = User(username=data['username'])                              # Создаем нового пользователя
    db.session.add(new_user)                                                # Добавляем пользователя в сессию базы данных
    db.session.commit()                                                     # Сохраняем изменения в базе данных
    # Возвращаем ответ с данными о созданном пользователе
    return jsonify({'message': 'User created', 'user': {'id': new_user.id, 'username': new_user.username}}), 201

# Точка доступа для создания новой публикации
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()                                               # Получаем данные из запроса
    new_post = Post(title=data['title'], content=data['content'], user_id=data['user_id']) # Создаем новую публикацию
    db.session.add(new_post)                                                # Добавляем публикацию в сессию базы данных
    db.session.commit()                                                     # Сохраняем изменения в базе данных
    # Возвращаем ответ с данными о созданной публикации
    return jsonify({'message': 'Post created', 'post': {'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'user_id': new_post.user_id}}), 201

# Точка доступа для получения всех публикаций
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()                                                # Запрашиваем все публикации из базы данных
    output = []                                                             # Формируем список публикаций для ответа
    for post in posts:
        post_data = {'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id}
        output.append(post_data)
    return jsonify({'posts': output})                                       # Возвращаем список публикаций

# Точка доступа для получения конкретной публикации по ID
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)                                   # Запрашиваем публикацию по ID
    # Возвращаем данные о публикации
    return jsonify({'post': {'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id}})

# Точка доступа для обновления публикации
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)                                   # Запрашиваем публикацию по ID
    data = request.get_json()                                               # Получаем данные из запроса
    post.title = data['title']                                              # Обновляем данные публикации
    post.content = data['content']
    db.session.commit()                                                     # Сохраняем изменения в базе данных
    # Возвращаем обновленные данные о публикации
    return jsonify({'message': 'Post updated', 'post': {'id': post.id, 'title': post.title, 'content': post.content}})

# Точка доступа для удаления публикации
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)                                  # Запрашиваем публикацию по ID
    db.session.delete(post)                                                # Удаляем публикацию из базы данных
    db.session.commit()                                                    # Сохраняем изменения в базе данных
    return jsonify({'message': 'Post deleted'})                            # Возвращаем сообщение об успешном удалении

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
