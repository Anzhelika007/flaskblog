from flask import Flask, render_template, redirect, request, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess'
db = SQLAlchemy(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Hashtag %r>' % self.name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    cover = db.Column(db.String(50), nullable=False, default='default.png')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('articles', lazy=True))
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtag.id'), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100))
    avatar = db.Column(db.String(50), nullable=False, default='default_user.png')

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/favorites')
def favorites():
    return render_template('favorites_posts.html')


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    password1 = request.form.get('password1')
    avatar = request.form.get('inputGroupFile04')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect('/login')

    if password == password1:
        new_user = User(email=email, username=username, avatar=avatar,
                        password=generate_password_hash(password, method='sha256'))
    else:
        print('password not true')
        return redirect('/register')

    db.session.add(new_user)
    db.session.commit()

    return redirect('/login')


@app.route('/login')
def login():
    return render_template('login_enter.html')


@app.route('/logout')
def logout():
    return 'Logout'


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'User page: ' + name + '-' + str(id)


@app.route('/post')
def post():
    return render_template('post.html')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
