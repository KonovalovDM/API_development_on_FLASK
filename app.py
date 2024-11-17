from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created', 'user': {'id': new_user.id, 'username': new_user.username}}), 201

# Endpoint to create a new post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'], user_id=data['user_id'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created', 'post': {'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'user_id': new_post.user_id}}), 201

# Endpoint to get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    output = []
    for post in posts:
        post_data = {'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id}
        output.append(post_data)
    return jsonify({'posts': output})

# Endpoint to get a specific post by ID
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({'post': {'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id}})

# Endpoint to update a post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Post updated', 'post': {'id': post.id, 'title': post.title, 'content': post.content}})

# Endpoint to delete a post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})

if __name__ == '__main__':
    app.run(debug=True)
