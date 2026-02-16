# all posts related routes
from extensions import db
from flask import request, jsonify, Blueprint
from models import Post
from decorators import token_required
from validation import PostSchema, ValidationError

post_bp = Blueprint('post', __name__)

@post_bp.route('/posts', methods=['POST'])
@token_required
def create_post():
    schema = PostSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    post = Post(
        title=data['title'],
        content=data['content'],
        user_id=request.user_id
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created', 'post_id': post.id}), 201

@post_bp.route('/posts/<int:post_id>', methods=['PUT'])
@token_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    # Check for ownership
    if post.user_id != request.user_id:
        return jsonify({'message': 'You can only edit your own posts'}), 403

    schema = PostSchema(partial=True)  
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']

    db.session.commit()
    return jsonify({'message': 'Post updated'}), 200

@post_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    # Allow if owner or admin
    if post.user_id != request.user_id and request.user_role != 'admin':
        return jsonify({'message': 'Unauthorized to delete this post'}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'}), 200

@post_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    output = []
    for post in posts:
        output.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at
        })
    return jsonify(output), 200
