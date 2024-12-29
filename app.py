import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from models import Post, Comment

# 创建 Flask 应用
app = Flask(__name__)

# 确保 instance 文件夹存在
os.makedirs(app.instance_path, exist_ok=True)

# 配置
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'mood_share.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db.init_app(app)

# 定义心情选项
MOODS = {
    'happy': {'emoji': '😊', 'color': '#FF7676', 'name': '开心'},
    'calm': {'emoji': '😌', 'color': '#7676FF', 'name': '平静'},
    'excited': {'emoji': '🤩', 'color': '#FFB876', 'name': '兴奋'},
    'touched': {'emoji': '🥺', 'color': '#9876FF', 'name': '感动'},
    'poop': {'emoji': '💩', 'color': '#8B4513', 'name': '拉屎'},
    'angry': {'emoji': '🤬', 'color': '#FF4444', 'name': '暴怒'},
    'sleepy': {'emoji': '🤤', 'color': '#FF44FF', 'name': '困饱'},
}

# 定义头像选项
AVATARS = [
    {'emoji': '🐱', 'name': '小猫'},
    {'emoji': '🐶', 'name': '小狗'},
    {'emoji': '🐰', 'name': '兔子'},
    {'emoji': '🐼', 'name': '熊猫'},
    {'emoji': '🦊', 'name': '狐狸'},
    {'emoji': '🐨', 'name': '考拉'}
]


@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts, moods=MOODS, avatars=AVATARS)


@app.route('/post', methods=['POST'])
def create_post():
    content = request.form.get('content')
    mood = request.form.get('mood')
    avatar_index = int(request.form.get('avatar', 0))
    author_name = request.form.get('author_name', '匿名用户')

    if content and mood in MOODS:
        post = Post(
            content=content,
            mood=mood,
            author_name=author_name,
            avatar=avatar_index
        )
        db.session.add(post)
        db.session.commit()
        flash('发布成功！')
    return redirect(url_for('index'))


@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return jsonify({'success': True, 'likes': post.likes})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)