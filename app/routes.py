from flask import Blueprint, request, jsonify
from app.database import db
from app.models import User, Post

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Главная страница."""
    return "Welcome to the API!"


@main_bp.route('/users', methods=['POST'])
def create_user():
    """Создает нового пользователя."""
    data = request.get_json()
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created', 'user': {'id': new_user.id, 'username': new_user.username}}), 201


@main_bp.route('/posts', methods=['POST'])
def create_post():
    """Создает новую публикацию."""
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'], user_id=data['user_id'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created', 'post': {'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'user_id': new_post.user_id}}), 201


@main_bp.route('/posts', methods=['GET'])
def get_posts():
    """Возвращает список всех публикаций."""
    posts = Post.query.all()
    output = [{'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id} for post in posts]
    return jsonify({'posts': output})


@main_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Возвращает данные конкретной публикации по ID."""
    post = Post.query.get_or_404(post_id)
    return jsonify({'post': {'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id}})


@main_bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Обновляет данные публикации."""
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Post updated', 'post': {'id': post.id, 'title': post.title, 'content': post.content}})


@main_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Удаляет публикацию."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})
